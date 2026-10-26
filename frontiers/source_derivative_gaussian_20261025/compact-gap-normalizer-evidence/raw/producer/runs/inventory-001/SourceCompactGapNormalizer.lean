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
open I4PeanoErrorBounds I4ConfluentIntegralIdentities ResearchFormalCoreR1
open scoped BigOperators Topology NNReal Interval

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
    (hr : 0 ≤ r) (hr1 : r ≤ 1) (_hB : 0 ≤ B) (hK : 0 ≤ K) (hJ : 0 ≤ J)
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
    [IsFiniteMeasure Q] (η H : ℝ) (hη : 0 < η) (_hH : 0 ≤ H)
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
      change A < sourceGammaRadius L ω at h
      change A ≤ sourceGammaRadius L ω
      exact h.le
    have htail := mul_le_mul_of_nonneg_left (measureReal_mono (μ := Q) hsub) hA.le
    have hbound := htail.trans (hMarkov.trans hmoment)
    nlinarith
  have hsubtract := le_measureReal_sdiff (μ := Q)
    (s₁ := {ω | sourceQ L ω ∈ Icc (-2 : ℝ) (-1)})
    (s₂ := {ω | A < sourceGammaRadius L ω})
  have heq : {ω | sourceQ L ω ∈ Icc (-2 : ℝ) (-1)} \
      {ω | A < sourceGammaRadius L ω} = sourceCompactGoodEvent L A := by
    ext ω
    change (sourceQ L ω ∈ Icc (-2 : ℝ) (-1) ∧ ¬ A < sourceGammaRadius L ω) ↔
      (sourceQ L ω ∈ Icc (-2 : ℝ) (-1) ∧ sourceGammaRadius L ω ≤ A)
    simp only [not_lt]
  rw [heq] at hsubtract
  dsimp only [A] at hsubtract
  linarith


/- Deterministic section supplied frozen by /root/compact_normalizer_deterministic. -/

/-- Translate the established cubic error theorem to any literal cubic target. -/
theorem cubic_pin_pointwise_error_target (g : ℝ → ℝ) (hgc : Continuous g)
    (C r c : ℝ) (hC : 0 ≤ C) (hr : 0 ≤ r)
    (hlip : ∀ x y : ℝ, |g x - g y| ≤ C * |x-y|)
    (hpin : 6 * (∫ t in (-1/2 : ℝ)..(1/2 : ℝ), peanoCubic t * g (r*t)) = c)
    (u : ℝ) (hu : u ∈ Icc (-1/2 : ℝ) (1/2 : ℝ)) :
    |g (r*u) - c| ≤ r*C := by
  let f : ℝ → ℝ := fun x => g x-c+2
  have hfc : Continuous f := (hgc.sub continuous_const).add continuous_const
  have hfl (x y : ℝ) : |f x-f y| ≤ C*|x-y| := by
    simpa only [f, show g x-c+2-(g y-c+2) = g x-g y by ring] using hlip x y
  have hmass : (∫ t in (-1/2 : ℝ)..(1/2 : ℝ), peanoCubic t) = 1/6 := by
    linarith [peano_kernel_masses.2.2.2]
  have hcK : Continuous peanoCubic := by unfold peanoCubic; fun_prop
  have hiG : IntervalIntegrable (fun t => peanoCubic t*g (r*t)) volume
      (-1/2 : ℝ) (1/2 : ℝ) :=
    (hcK.mul (hgc.comp (continuous_const.mul continuous_id))).intervalIntegrable _ _
  have hiC : IntervalIntegrable (fun t => peanoCubic t*c) volume
      (-1/2 : ℝ) (1/2 : ℝ) := (hcK.mul continuous_const).intervalIntegrable _ _
  have hi2 : IntervalIntegrable (fun t => peanoCubic t*2) volume
      (-1/2 : ℝ) (1/2 : ℝ) := (hcK.mul continuous_const).intervalIntegrable _ _
  have hfp : 6*(∫ t in (-1/2 : ℝ)..(1/2 : ℝ), peanoCubic t*f (r*t)) = 2 := by
    simp_rw [f, mul_add, mul_sub]
    rw [intervalIntegral.integral_add (hiG.sub hiC) hi2,
      intervalIntegral.integral_sub hiG hiC,
      intervalIntegral.integral_mul_const, intervalIntegral.integral_mul_const, hmass]
    linarith
  have h := cubic_pin_pointwise_error f hfc C r hC hr hfl hfp u hu
  simpa only [f, show g (r*u)-c+2-2 = g (r*u)-c by ring] using h

/-- Literal axial centers for arbitrary cubic-gap pin 12*k. -/
theorem source_normalized_gap_axial_errors {L : ℝ} (hL : L ≠ 0)
    (r k : ℝ) (hr : 0 < r) (sample : SmoothSample 2 L)
    (h3 : sourceConfluentPinsAt L r sample 3 = 0)
    (h4 : sourceConfluentPinsAt L r sample 4 = 0)
    (h5 : sourceConfluentPinsAt L r sample 5 = 12*k) :
    |sourceNormalizedEndpoints L r sample 0 + 6*k| ≤ r*sourceGammaRadius L sample ∧
    |sourceNormalizedEndpoints L r sample 1 - 6*k| ≤ r*sourceGammaRadius L sample := by
  have hΓ4 := sourceDerivativeMajorant_nonneg L 4 sample
  have hpin := pin5_integral (sourceF L sample) (sourceF_C3 hL sample) r hr.ne'
  rw [← source_pin5_eq hL r sample,h5] at hpin
  have hf := cubic_pin_pointwise_error_target _ (sourceF_third_continuous hL sample)
    _ r (12*k) hΓ4 hr.le (sourceF_third_lipschitz hL sample) hpin.symm
  have hleft := left_weighted_error _ (sourceF_third_continuous hL sample) r (12*k)
    (r*sourceDerivativeMajorant L 4 sample) hf
  have hright := right_weighted_error _ (sourceF_third_continuous hL sample) r (12*k)
    (r*sourceDerivativeMajorant L 4 sample) hf
  have hbound : r*sourceDerivativeMajorant L 4 sample/2 ≤ r*sourceGammaRadius L sample := by
    have hm : r*sourceDerivativeMajorant L 4 sample ≤ r*sourceGammaRadius L sample :=
      mul_le_mul_of_nonneg_left (sourceDerivativeMajorant_le_radius L sample 4) hr.le
    linarith [mul_nonneg hr.le hΓ4]
  rw [source_normalized_peano hL r hr.ne' sample h3 h4]
  constructor
  · change |-(∫ u in (-1/2:ℝ)..(1/2:ℝ),
        peanoLeft u * iteratedDeriv 3 (sourceF L sample) (r*u)) + 6*k| ≤ _
    have heq : (12*k)/2 = 6*k := by ring
    rw [heq] at hleft
    simpa only [show -(∫ u in (-1/2:ℝ)..(1/2:ℝ),
      peanoLeft u * iteratedDeriv 3 (sourceF L sample) (r*u)) + 6*k =
      -((∫ u in (-1/2:ℝ)..(1/2:ℝ),
        peanoLeft u * iteratedDeriv 3 (sourceF L sample) (r*u))-6*k) by ring,
      abs_neg] using hleft.trans hbound
  · change |(∫ u in (-1/2:ℝ)..(1/2:ℝ),
        peanoRight u * iteratedDeriv 3 (sourceF L sample) (r*u)) - 6*k| ≤ _
    have heq : (12*k)/2 = 6*k := by ring
    rw [heq] at hright
    exact hright.trans hbound

/-- Finite physical-Hessian arithmetic retaining the literal strict type branch. -/
theorem endpointWeight_gap_floor (r k k0 A q : ℝ) (v : Fin 6 → ℝ)
    (hr : 0 < r) (hk0 : 0 < k0) (hk : k0 ≤ k) (hA : 1 ≤ A)
    (hrδ : r < min 1 (min (1/(2*A)) (k0/(2*A^2))))
    (hq : q ∈ Icc (-2 : ℝ) (-1 : ℝ))
    (h0 : |v 0+6*k| ≤ r*A) (h1 : |v 1-6*k| ≤ r*A)
    (h2 : |v 2| ≤ A) (h3 : |v 3| ≤ A)
    (h4 : |v 4-q| ≤ r*A) (h5 : |v 5-q| ≤ r*A) :
    (dm2Negative (egm_HM r (sourcePhysicalCoordinates v)) ∧
      (egm_HS r (sourcePhysicalCoordinates v)).det < 0) ∧
    k0^2*r^2 ≤ sourceEndpointWeight r v := by
  have hA0 : 0 < A := by linarith
  have hrA : r*A < 1/2 := by
    have h := (lt_div_iff₀ (by positivity : 0 < 2*A)).mp
      (lt_of_lt_of_le hrδ (min_le_of_right_le (min_le_left _ _)))
    nlinarith
  have hrAA : r*A^2 < k0/2 := by
    have h := (lt_div_iff₀ (by positivity : 0 < 2*A^2)).mp
      (lt_of_lt_of_le hrδ (min_le_of_right_le (min_le_right _ _)))
    nlinarith
  have hAA : A ≤ A^2 := by nlinarith
  have hrAk : r*A < k0/2 :=
    (mul_le_mul_of_nonneg_left hAA hr.le).trans_lt hrAA
  have hv0 : v 0 ≤ -3*k0 := by
    have h := (abs_le.mp h0).2
    linarith
  have hv1 : 3*k0 ≤ v 1 := by
    have h := (abs_le.mp h1).1
    linarith
  have hv4 : v 4 ≤ -1/2 := by
    have h := (abs_le.mp h4).2
    linarith [hq.2]
  have hv5 : v 5 ≤ -1/2 := by
    have h := (abs_le.mp h5).2
    linarith [hq.2]
  have hb2 : (v 2)^2 ≤ A^2 := by
    simpa only [sq_abs] using pow_le_pow_left₀ (abs_nonneg (v 2)) h2 2
  have hb3 : (v 3)^2 ≤ A^2 := by
    simpa only [sq_abs] using pow_le_pow_left₀ (abs_nonneg (v 3)) h3 2
  have hMprod : 3*k0/2 ≤ v 0*v 4 := by
    calc
      3*k0/2 = (-3*k0)*(-1/2) := by ring
      _ ≤ (-3*k0)*v 4 := mul_le_mul_of_nonpos_left hv4 (by linarith)
      _ ≤ v 0*v 4 := mul_le_mul_of_nonpos_right hv0 (by linarith)
  have hSprod : v 1*v 5 ≤ -3*k0/2 := by
    calc
      _ ≤ (3*k0)*v 5 := mul_le_mul_of_nonpos_right hv1 (by linarith)
      _ ≤ (3*k0)*(-1/2) := mul_le_mul_of_nonneg_left hv5 (by positivity)
      _ = _ := by ring
  have hDM : k0 ≤ v 0*v 4-r*(v 2)^2 := by
    have h := mul_le_mul_of_nonneg_left hb2 hr.le
    linarith
  have hDS : v 1*v 5-r*(v 3)^2 ≤ -3*k0/2 := by
    linarith [mul_nonneg hr.le (sq_nonneg (v 3))]
  have hdetM : (egm_HM r (sourcePhysicalCoordinates v)).det =
      r*(v 0*v 4-r*(v 2)^2) := by
    simp [egm_HM,sourcePhysicalCoordinates,Matrix.det_fin_two]
    ring
  have hdetS : (egm_HS r (sourcePhysicalCoordinates v)).det =
      r*(v 1*v 5-r*(v 3)^2) := by
    simp [egm_HS,sourcePhysicalCoordinates,Matrix.det_fin_two]
    ring
  have htype : dm2Negative (egm_HM r (sourcePhysicalCoordinates v)) ∧
      (egm_HS r (sourcePhysicalCoordinates v)).det < 0 := by
    constructor
    · change dm2Negative !![r*v 0,r*v 2;r*v 2,v 4]
      rw [dm2_negative_iff]
      constructor
      · exact mul_neg_of_pos_of_neg hr (by linarith)
      · have hp : 0 < r*(v 0*v 4-r*(v 2)^2) := mul_pos hr (lt_of_lt_of_le hk0 hDM)
        nlinarith only [hp]
    · rw [hdetS]
      exact mul_neg_of_pos_of_neg hr (by linarith)
  refine ⟨htype,?_⟩
  rw [sourceEndpointWeight,egm_weight,ite_eq_left htype,hdetM,hdetS]
  have hDS' : k0 ≤ -(v 1*v 5-r*(v 3)^2) := by linarith
  have hp := mul_le_mul hDM hDS' hk0.le (lt_of_lt_of_le hk0 hDM).le
  have hsign : r*(v 0*v 4-r*(v 2)^2)*(r*(v 1*v 5-r*(v 3)^2)) ≤ 0 :=
    mul_nonpos_of_nonneg_of_nonpos
      (mul_nonneg hr.le (lt_of_lt_of_le hk0 hDM).le)
      (mul_nonpos_of_nonneg_of_nonpos hr.le (by linarith))
  rw [abs_of_nonpos hsign]
  have hmul := mul_le_mul_of_nonneg_left hp (sq_nonneg r)
  nlinarith only [hmul]

/-- Actual physical weight floor on the bounded-radius, negative-q event.
Only Hessian typing is asserted; endpoint criticality needs the gradient pins. -/
theorem sourceSmoothWeight_gap_floor {L : ℝ} (hL : L ≠ 0)
    (r k k0 A : ℝ) (hr : 0 < r) (hk0 : 0 < k0) (hk : k0 ≤ k) (hA : 1 ≤ A)
    (hrδ : r < min 1 (min (1/(2*A)) (k0/(2*A^2))))
    (sample : SmoothSample 2 L)
    (h3 : sourceConfluentPinsAt L r sample 3 = 0)
    (h4 : sourceConfluentPinsAt L r sample 4 = 0)
    (h5 : sourceConfluentPinsAt L r sample 5 = 12*k)
    (hq : sourceQ L sample ∈ Icc (-2 : ℝ) (-1 : ℝ))
    (hΓ : sourceGammaRadius L sample ≤ A) :
    sourceSmoothTyped L r sample ∧ k0^2*r^2 ≤ sourceSmoothWeight L r sample := by
  obtain ⟨ha0,ha1⟩ := source_normalized_gap_axial_errors hL r k hr sample h3 h4 h5
  have hcross := source_normalized_first_four_bound hL r hr.ne' sample h3 h4
  obtain ⟨ht4,ht5⟩ := source_normalized_transverse_errors hL r hr.le sample
  have hΓ3 := (sourceDerivativeMajorant_le_radius L sample 3).trans hΓ
  have hrΓ := mul_le_mul_of_nonneg_left hΓ hr.le
  have hrΓ3 := mul_le_mul_of_nonneg_left hΓ3 hr.le
  obtain ⟨ht,hW⟩ := endpointWeight_gap_floor r k k0 A (sourceQ L sample)
    (sourceNormalizedEndpoints L r sample) hr hk0 hk hA hrδ hq
    (ha0.trans hrΓ) (ha1.trans hrΓ) ((hcross 2).trans hΓ) ((hcross 3).trans hΓ)
    (ht4.trans hrΓ3) (ht5.trans hrΓ3)
  constructor
  · unfold sourceSmoothTyped
    rw [sourceRawHM_eq_normalized L r hr.ne' sample,
      sourceRawHS_eq_normalized L r hr.ne' sample]
    exact ht
  · rw [sourceSmoothWeight_eq L r hr.ne' sample]
    exact hW


/-- A uniform positive quadratic normalizer floor under the literal actual gap law.
All constants are chosen before radius, height and positive gap coefficient. -/
theorem sourceGapLaw_compact_normalizer {L : ℝ} (hL : L ≠ 0)
    (B k0 k1 : ℝ) (hB : 0 ≤ B) (hk0 : 0 < k0) (hk01 : k0 ≤ k1) :
    ∃ c δ : ℝ, 0 < c ∧ 0 < δ ∧ δ ≤ 1 ∧
      ∀ r : ℝ, 0 < r → r < δ → ∀ b k : ℝ, |b| ≤ B → k0 ≤ k → k ≤ k1 →
        Integrable (sourceSmoothWeight L r) (sourceGapLaw hL r b k) ∧
        c*r^2 ≤ ∫ sample, sourceSmoothWeight L r sample ∂sourceGapLaw hL r b k := by
  have hk1 : 0 ≤ k1 := hk0.le.trans hk01
  obtain ⟨η,δq,hη,hδq,hδq1,hqmass⟩ :=
    sourceGapLaw_negative_interval_mass hL B k1 hB hk1
  obtain ⟨δm,hδm,_hδm1,hmoments⟩ := sourceGapLaw_height_moments hL k1 hk1
  obtain ⟨C,hC,hmoment⟩ := hmoments 1
  obtain ⟨δi,hδi,_hδi1,hintegrable⟩ := sourceGapLaw_weight_integrable hL
  obtain ⟨δp,hδp,_hδp1,hpins⟩ := sourceGapLaw_curvature_bounds hL
  let H := C*(1+B)
  have hH : 0 ≤ H := mul_nonneg hC (by linarith)
  let A := max 1 (2*H/η)
  have hA : 1 ≤ A := le_max_left _ _
  have hA0 : 0 < A := lt_of_lt_of_le (by norm_num) hA
  let δdet := min 1 (min (1/(2*A)) (k0/(2*A^2)))
  have hδdet : 0 < δdet := by dsimp [δdet]; positivity
  let δ := min δq (min δm (min δi (min δp δdet)))
  have hδ : 0 < δ := lt_min hδq (lt_min hδm (lt_min hδi (lt_min hδp hδdet)))
  refine ⟨k0^2*η/2,δ,by positivity,hδ,(min_le_left _ _).trans hδq1,?_⟩
  intro r hr hrδ b k hb hk hk'
  have hrq : r < δq := hrδ.trans_le (min_le_left _ _)
  have hrm : r < δm := hrδ.trans_le (min_le_of_right_le (min_le_left _ _))
  have hri : r < δi := hrδ.trans_le
    (min_le_of_right_le (min_le_of_right_le (min_le_left _ _)))
  have hrp : r < δp := hrδ.trans_le
    (min_le_of_right_le (min_le_of_right_le (min_le_of_right_le (min_le_left _ _))))
  have hrdet : r < δdet := hrδ.trans_le
    (min_le_of_right_le (min_le_of_right_le (min_le_of_right_le (min_le_right _ _))))
  have hkabs : |k| ≤ k1 := by rw [abs_of_nonneg (hk0.le.trans hk)]; exact hk'
  let Q := sourceGapLaw hL r b k
  have : IsProbabilityMeasure Q := by
    change IsProbabilityMeasure (sourceSmoothKernel hL r (sourceGapPins r b k))
    infer_instance
  have hW : Integrable (sourceSmoothWeight L r) Q := hintegrable r hr hri b k
  obtain ⟨hΓ1,hΓbound⟩ := hmoment r hr hrm b k hkabs
  have hΓ : Integrable (sourceGammaRadius L) Q := by simpa only [pow_one] using hΓ1
  have hmomentH : (∫ ω, sourceGammaRadius L ω ∂Q) ≤ H := by
    have hheight : C*(1+|b|) ≤ C*(1+B) :=
      mul_le_mul_of_nonneg_left (add_le_add le_rfl hb) hC
    have hb' : (∫ ω, sourceGammaRadius L ω ∂Q) ≤ C*(1+|b|) := by
      simpa only [pow_one] using hΓbound
    exact hb'.trans hheight
  have hgood : η/2 ≤ Q.real (sourceCompactGoodEvent L A) :=
    sourceCompactGoodEvent_mass Q η H hη hH hΓ hmomentH (hqmass r hr hrq b k hb hkabs)
  have hmeas := sourceCompactGoodEvent_measurable hL A
  have hInd : Integrable ((sourceCompactGoodEvent L A).indicator
      (fun _ : SmoothSample 2 L => k0^2*r^2)) Q := (integrable_const _).indicator hmeas
  have hpoint : (sourceCompactGoodEvent L A).indicator
      (fun _ : SmoothSample 2 L => k0^2*r^2) ≤ᵐ[Q] sourceSmoothWeight L r := by
    filter_upwards [hpins r hr hrp b k] with sample hs
    by_cases he : sample ∈ sourceCompactGoodEvent L A
    · rw [Set.indicator_of_mem he]
      have h3 : sourceConfluentPinsAt L r sample 3 = 0 := by rw [hs.1]; simp [sourceGapPins]
      have h4 : sourceConfluentPinsAt L r sample 4 = 0 := by rw [hs.1]; simp [sourceGapPins]
      have h5 : sourceConfluentPinsAt L r sample 5 = 12*k := by rw [hs.1]; simp [sourceGapPins]
      exact (sourceSmoothWeight_gap_floor hL r k k0 A hr hk0 hk hA hrdet sample
        h3 h4 h5 he.1 he.2).2
    · rw [Set.indicator_of_notMem he]
      exact sourceSmoothWeight_nonneg L r sample
  have hintegral := integral_mono_ae hInd hW hpoint
  have heq : (∫ sample, (sourceCompactGoodEvent L A).indicator
      (fun _ : SmoothSample 2 L => k0^2*r^2) sample ∂Q) =
      k0^2*r^2*Q.real (sourceCompactGoodEvent L A) := by
    rw [integral_indicator hmeas,setIntegral_const,smul_eq_mul]
    ring
  rw [heq] at hintegral
  refine ⟨hW,?_⟩
  calc
    (k0^2*η/2)*r^2 = k0^2*r^2*(η/2) := by ring
    _ ≤ k0^2*r^2*Q.real (sourceCompactGoodEvent L A) :=
      mul_le_mul_of_nonneg_left hgood (by positivity)
    _ ≤ ∫ sample, sourceSmoothWeight L r sample ∂Q := hintegral

end SourceCompactGapNormalizer
