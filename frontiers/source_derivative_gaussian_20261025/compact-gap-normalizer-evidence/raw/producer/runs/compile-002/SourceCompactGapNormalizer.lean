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

/- Gaussian lower section supplied frozen by /root/compact_normalizer_gaussian. -/

/-- A positive lower density on the fixed negative unit interval. -/
def gaussianCompactLowerConstant (V M : ℝ) : ℝ :=
  (Real.sqrt (4 * Real.pi * V))⁻¹ * Real.exp (-(2 + M)^2 / V)

theorem gaussianCompactLowerConstant_pos {V : ℝ} (M : ℝ) (hV : 0 < V) :
    0 < gaussianCompactLowerConstant V M := by
  unfold gaussianCompactLowerConstant
  positivity

/-- The prefactor uses the variance upper bound, and the exponent the lower bound. -/
theorem gaussianPDFReal_lower_compact (V M μ : ℝ) (ν : ℝ≥0)
    (hV : 0 < V) (hM : 0 ≤ M) (hμ : |μ| ≤ M)
    (hνlo : V / 2 ≤ (ν : ℝ)) (hνhi : (ν : ℝ) ≤ 2 * V)
    {x : ℝ} (hx : x ∈ Icc (-2 : ℝ) (-1)) :
    gaussianCompactLowerConstant V M ≤ gaussianPDFReal μ ν x := by
  have hνpos : 0 < (ν : ℝ) := by linarith
  have hxabs : |x| ≤ 2 := abs_le.mpr ⟨hx.1, by linarith [hx.2]⟩
  have hdist : |x - μ| ≤ 2 + M :=
    (abs_sub x μ).trans (add_le_add hxabs hμ)
  have hsq : (x - μ)^2 ≤ (2 + M)^2 := by
    nlinarith [sq_abs (x - μ), abs_nonneg (x - μ)]
  have hden : V ≤ 2 * (ν : ℝ) := by linarith
  have hquot : (x - μ)^2 / (2 * (ν : ℝ)) ≤ (2 + M)^2 / V :=
    (div_le_div_of_nonneg_right hsq (by positivity)).trans
      (div_le_div_of_nonneg_left (sq_nonneg (2 + M)) hV hden)
  have hexp : Real.exp (-(2 + M)^2 / V) ≤
      Real.exp (-(x - μ)^2 / (2 * (ν : ℝ))) := by
    apply Real.exp_le_exp.mpr
    simpa only [neg_div] using neg_le_neg hquot
  have hsqrt : Real.sqrt (2 * Real.pi * (ν : ℝ)) ≤
      Real.sqrt (4 * Real.pi * V) := by
    apply Real.sqrt_le_sqrt
    calc
      2 * Real.pi * (ν : ℝ) ≤ 2 * Real.pi * (2 * V) :=
        mul_le_mul_of_nonneg_left hνhi (by positivity)
      _ = 4 * Real.pi * V := by ring
  have hpref : (Real.sqrt (4 * Real.pi * V))⁻¹ ≤
      (Real.sqrt (2 * Real.pi * (ν : ℝ)))⁻¹ :=
    inv_anti₀ (by positivity) hsqrt
  exact mul_le_mul hpref hexp (by positivity) (by positivity)

/-- Integration of the lower PDF over an interval of length one. -/
theorem gaussianReal_Icc_lower_compact (V M μ : ℝ) (ν : ℝ≥0)
    (hV : 0 < V) (hM : 0 ≤ M) (hμ : |μ| ≤ M)
    (hνlo : V / 2 ≤ (ν : ℝ)) (hνhi : (ν : ℝ) ≤ 2 * V) :
    gaussianCompactLowerConstant V M ≤ (gaussianReal μ ν).real (Icc (-2 : ℝ) (-1)) := by
  have hνpos : 0 < (ν : ℝ) := by linarith
  have hνne : ν ≠ 0 := by
    intro h
    simp [h] at hνpos
  have hnonneg : 0 ≤ ∫ x in Icc (-2 : ℝ) (-1), gaussianPDFReal μ ν x :=
    integral_nonneg (fun x => gaussianPDFReal_nonneg μ ν x)
  have heq : (gaussianReal μ ν).real (Icc (-2 : ℝ) (-1)) =
      ∫ x in Icc (-2 : ℝ) (-1), gaussianPDFReal μ ν x := by
    rw [measureReal_def, gaussianReal_apply_eq_integral μ hνne,
      ENNReal.toReal_ofReal hnonneg]
  have hconst : IntegrableOn (fun _ : ℝ => gaussianCompactLowerConstant V M)
      (Icc (-2 : ℝ) (-1)) := continuous_const.integrableOn_Icc
  rw [heq]
  calc
    gaussianCompactLowerConstant V M =
        ∫ x in Icc (-2 : ℝ) (-1), gaussianCompactLowerConstant V M := by
      rw [setIntegral_const, smul_eq_mul, Real.volume_real_Icc_of_le (by norm_num :
        (-2 : ℝ) ≤ -1)]
      norm_num
    _ ≤ ∫ x in Icc (-2 : ℝ) (-1), gaussianPDFReal μ ν x :=
      setIntegral_mono_on hconst ((integrable_gaussianPDFReal μ ν).restrict)
        measurableSet_Icc (fun x hx => gaussianPDFReal_lower_compact V M μ ν
          hV hM hμ hνlo hνhi hx)


/-- The six-factor estimate uses the actual Pi norm, with the affine mean intact. -/
theorem sourceGap_curvatureMean_bound (L r b k B K J : ℝ)
    (hr : 0 ≤ r) (hr1 : r ≤ 1) (hB : 0 ≤ B) (hK : 0 ≤ K) (hJ : 0 ≤ J)
    (hb : |b| ≤ B) (hk : |k| ≤ K)
    (hβ : ∀ i, |curvatureBeta L r i| ≤ J) :
    |curvatureMean L r (sourceGapPins r b k)| ≤ 6*J*(B+13*K) := by
  have hp := (sourceGapPins_norm_le r b k K hr hr1 hK hk).trans
    (add_le_add hb le_rfl)
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

/-- A common negative-interval mass for bounded heights and bounded gaps. -/
theorem sourceGapLaw_negative_interval_mass {L : ℝ} (hL : L ≠ 0)
    (B K : ℝ) (hB : 0 ≤ B) (hK : 0 ≤ K) :
    ∃ η δ : ℝ, 0 < η ∧ 0 < δ ∧ δ ≤ 1 ∧
      ∀ r : ℝ, 0 < r → r < δ → ∀ b k : ℝ, |b| ≤ B → |k| ≤ K →
        η ≤ (sourceGapLaw hL r b k).real
          {ω | sourceQ L ω ∈ Icc (-2 : ℝ) (-1)} := by
  obtain ⟨J,_N,δ,hJ,_hN,hδ,hδ1,hbounds⟩ := curvature_uniform_parameter_bounds hL 0
  let V := sourceContactSchur L
  have hV : 0 < V := sourceContactSchur_pos hL
  have hvup : ∀ᶠ r in 𝓝[>] (0 : ℝ), curvatureVariance L r < 2*V :=
    (curvatureVariance_tendsto hL).eventually (gt_mem_nhds (by dsimp [V]; linarith))
  obtain ⟨ε,hε,hup⟩ := mem_nhdsGT_iff_exists_Ioo_subset.mp hvup
  let M := 6*J*(B+13*K)
  have hM : 0 ≤ M := by dsimp [M]; positivity
  refine ⟨gaussianCompactLowerConstant V M,min δ ε,
    gaussianCompactLowerConstant_pos M hV,lt_min hδ hε,
    (min_le_left _ _).trans hδ1,?_⟩
  intro r hr hrδ b k hb hk
  have hrδ' := hrδ.trans_le (min_le_left _ _)
  obtain ⟨hG,hlo,hβ,_hmean⟩ := hbounds r hr hrδ'
  have hhi : curvatureVariance L r ≤ 2*V :=
    (hup ⟨hr,hrδ.trans_le (min_le_right _ _)⟩).le
  have hτ : 0 < curvatureVariance L r := by change V/2 ≤ _ at hlo; linarith
  have hμ : |curvatureMean L r (sourceGapPins r b k)| ≤ M :=
    sourceGap_curvatureMean_bound L r b k B K J hr.le
      (hrδ'.le.trans hδ1) hB hK hJ hb hk hβ
  rw [(sourceGapLaw_q_hasLaw hL r b k hG hτ).measureReal_eq
    (p := fun q => q ∈ Icc (-2 : ℝ) (-1)) measurableSet_Icc]
  apply gaussianReal_Icc_lower_compact V M _ _ hV hM hμ
  · rwa [Real.coe_toNNReal _ hτ.le]
  · rwa [Real.coe_toNNReal _ hτ.le]

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
        {ω | A ≤ sourceGammaRadius L ω} := by
      intro ω h
      exact le_of_lt h
    have htail := mul_le_mul_of_nonneg_left (measureReal_mono hsub) hA.le
    have hbound := htail.trans (hMarkov.trans hmoment)
    nlinarith
  have hsubtract := le_measureReal_sdiff (μ := Q)
    (s₁ := {ω | sourceQ L ω ∈ Icc (-2 : ℝ) (-1)})
    (s₂ := {ω | A < sourceGammaRadius L ω})
  have heq : {ω | sourceQ L ω ∈ Icc (-2 : ℝ) (-1)} \
      {ω | A < sourceGammaRadius L ω} = sourceCompactGoodEvent L A := by
    ext ω
    change (_ ∧ ¬ A < sourceGammaRadius L ω) ↔ (_ ∧ sourceGammaRadius L ω ≤ A)
    simp only [not_lt]
  rw [heq] at hsubtract
  dsimp only [A] at hsubtract
  linarith

end SourceCompactGapNormalizer
