import SourceCompactTargetMoments
import SourceCurvatureDecomposition

/-!
# Whole-carrier all-target curvature residual bounds

The radius is the original Gamma of the literal posterior sample at every
six-vector target. One interval chosen from L != 0 controls reconstruction,
residual images and all polynomial moments under the actual residual law.
The covariance direction is independent of the target; its existing envelope
is taken at b=0. Existing whole-carrier scalar/product laws and densities are
reused without a second construction. No weighted or normalized probability
conclusion is asserted.
-/

noncomputable section

open I4Foundation I4Source I4Smooth I4SmoothCarrier I4SourceGaussian
open I4SourceDerivativeGaussian I4SourceConfluentPins I4SourceConfluentLimits
open I4SourceEndpointRegression I4SourceEndpointEstimates I4SourceSmoothConditional
open I4SourceConditionalMajorant I4SourcePinCurvatureBounds I4SourceSmoothPalm
open I4SourceCurvatureDecomposition I4SourceCompactTargetMoments I4GaussianMajorant
open I4SourceContact I4ContactGram MeasureTheory ProbabilityTheory Filter
open scoped BigOperators Topology

set_option autoImplicit false

namespace I4SourceAllTargetCurvatureResidual

/-- The original posterior radius, at every literal target. -/
def allTargetCurvatureResidualRadius {L : ℝ} (hL : L ≠ 0) (r : ℝ) (p : Fin 6 → ℝ) (ρ : SmoothSample 2 L) : ℝ :=
  sourceGammaRadius L (posteriorSample hL r p ρ)

theorem allTargetCurvatureResidualRadius_measurable {L : ℝ} (hL : L ≠ 0) (r : ℝ) (p : Fin 6 → ℝ) :
    Measurable (allTargetCurvatureResidualRadius hL r p) :=
  (sourceGammaRadius_measurable L).comp
    ((posteriorSample_measurable hL r).comp (measurable_const.prodMk measurable_id))

theorem one_le_allTargetCurvatureResidualRadius {L : ℝ} (hL : L ≠ 0) (r : ℝ) (p : Fin 6 → ℝ) (ρ : SmoothSample 2 L) :
    1 ≤ allTargetCurvatureResidualRadius hL r p ρ := one_le_sourceGammaRadius L _

theorem sourceContactQ_posterior_abs_le_allTargetRadius {L : ℝ} (hL : L ≠ 0) (r : ℝ) (p : Fin 6 → ℝ)
    (ρ : SmoothSample 2 L) :
    |sourceContactQ L (posteriorSample hL r p ρ)| ≤ allTargetCurvatureResidualRadius hL r p ρ := by
  exact (sourceQ_abs_le hL _).trans (sourceDerivativeMajorant_le_radius L _ (2 : Fin 6))

theorem sourceDerivativeMajorant_allTarget_curvatureReconstruct {L : ℝ} (hL : L ≠ 0) (r : ℝ) (p : Fin 6 → ℝ) (q : ℝ)
    (hσ : 0 < curvatureSigma L r) (U : SourceMode 2 → ℝ)
    (hU : ∀ m, 0 ≤ U m)
    (hUs : ∀ n : ℕ, Summable (fun m => orderModeBound n 2 L m * U m))
    (hχU : ∀ m, |curvatureDirection L r m|/curvatureSigma L r ≤ U m)
    (k : ℕ) (ρ : SmoothSample 2 L) :
    sourceDerivativeMajorant L k
      (curvatureReconstruct hL r p ρ q) ≤
      sourceDerivativeMajorant L k (posteriorSample hL r p ρ) +
        (∑' m, orderModeBound k 2 L m*U m)*(|q|+allTargetCurvatureResidualRadius hL r p ρ) := by
  let φ := posteriorSample hL r p ρ
  have hbase := φ.property k
  have hright := hbase.add ((hUs k).mul_right (|q|+allTargetCurvatureResidualRadius hL r p ρ))
  have hleft := (curvatureReconstruct hL r p ρ q).property k
  have hq : |q-sourceContactQ L φ| ≤ |q|+allTargetCurvatureResidualRadius hL r p ρ := by
    exact (abs_sub _ _).trans (add_le_add le_rfl (sourceContactQ_posterior_abs_le_allTargetRadius hL r p ρ))
  have ht0 : 0 ≤ |q|+allTargetCurvatureResidualRadius hL r p ρ := by
    have hs := one_le_allTargetCurvatureResidualRadius hL r p ρ
    linarith [abs_nonneg q]
  have hi (m : SourceMode 2) :
      orderModeBound k 2 L m * |(curvatureReconstruct hL r p ρ q).val m| ≤
      orderModeBound k 2 L m * |φ.val m| +
        (orderModeBound k 2 L m*U m)*(|q|+allTargetCurvatureResidualRadius hL r p ρ) := by
    change orderModeBound k 2 L m * |φ.val m + curvatureDirection L r m *
      ((q-sourceContactQ L φ)/curvatureSigma L r)| ≤ _
    have hshift : |curvatureDirection L r m * ((q-sourceContactQ L φ)/curvatureSigma L r)| ≤
        U m*(|q|+allTargetCurvatureResidualRadius hL r p ρ) := by
      rw [abs_mul, abs_div, abs_of_pos hσ]
      have heq : |curvatureDirection L r m| * (|q-sourceContactQ L φ|/curvatureSigma L r) =
          (|curvatureDirection L r m|/curvatureSigma L r)*|q-sourceContactQ L φ| := by ring
      rw [heq]
      exact mul_le_mul (hχU m) hq (abs_nonneg _) (hU m)
    calc
      _ ≤ orderModeBound k 2 L m * (|φ.val m| +
          |curvatureDirection L r m * ((q-sourceContactQ L φ)/curvatureSigma L r)|) :=
        mul_le_mul_of_nonneg_left (abs_add_le _ _) (orderModeBound_nonneg k 2 L m)
      _ ≤ orderModeBound k 2 L m * (|φ.val m|+U m*(|q|+allTargetCurvatureResidualRadius hL r p ρ)) :=
        mul_le_mul_of_nonneg_left (add_le_add le_rfl hshift) (orderModeBound_nonneg k 2 L m)
      _ = _ := by ring
  have h := hleft.tsum_le_tsum hi hright
  rw [hbase.tsum_add ((hUs k).mul_right _), tsum_mul_right] at h
  exact h

theorem sourceGammaRadius_allTarget_curvatureReconstruct {L : ℝ} (hL : L ≠ 0) (r : ℝ) (p : Fin 6 → ℝ) (q : ℝ)
    (hσ : 0 < curvatureSigma L r) (U : SourceMode 2 → ℝ)
    (hU : ∀ m, 0 ≤ U m)
    (hUs : ∀ n : ℕ, Summable (fun m => orderModeBound n 2 L m * U m))
    (hχU : ∀ m, |curvatureDirection L r m|/curvatureSigma L r ≤ U m)
    (ρ : SmoothSample 2 L) :
    sourceGammaRadius L (curvatureReconstruct hL r p ρ q) ≤
      (1+curvatureEnvelopeTotal L U)*(|q|+allTargetCurvatureResidualRadius hL r p ρ) := by
  have hpart (k : Fin 6) := sourceDerivativeMajorant_allTarget_curvatureReconstruct hL r p q hσ U hU hUs hχU k ρ
  have hs := Finset.sum_le_sum (fun k (_ : k ∈ (Finset.univ : Finset (Fin 6))) => hpart k)
  rw [Finset.sum_add_distrib, ← Finset.sum_mul] at hs
  change 1+∑ k : Fin 6, sourceDerivativeMajorant L k
      (curvatureReconstruct hL r p ρ q) ≤ _
  dsimp [allTargetCurvatureResidualRadius, sourceGammaRadius, curvatureEnvelopeTotal] at *
  nlinarith [abs_nonneg q]

theorem allTargetCurvatureResidualRadius_image_bound {L : ℝ} (hL : L ≠ 0) (r : ℝ) (p : Fin 6 → ℝ)
    (hG : IsUnit (sourcePinCovarianceAt L r)) (U : SourceMode 2 → ℝ)
    (hU : ∀ m, 0 ≤ U m)
    (hUs : ∀ n : ℕ, Summable (fun m => orderModeBound n 2 L m * U m))
    (hχU : ∀ m, |curvatureDirection L r m| ≤ U m) (ω : SmoothSample 2 L) :
    allTargetCurvatureResidualRadius hL r p (curvatureResidualSample hL r ω) ≤
      sourceGammaRadius L (posteriorSample hL r p ω) +
        curvatureEnvelopeTotal L U * |curvatureZ L r ω| := by
  unfold allTargetCurvatureResidualRadius
  rw [curvaturePosterior_residual_eq_shift hL r hG]
  simpa only [abs_neg] using sourceGammaRadius_curvatureShift hL r (-curvatureZ L r ω)
    U hU hUs hχU (posteriorSample hL r p ω)

theorem allTargetCurvatureResidualRadius_moment_bound {L : ℝ} (hL : L ≠ 0) (r : ℝ) (p : Fin 6 → ℝ)
    (hG : IsUnit (sourcePinCovarianceAt L r)) (hτ : 0 < curvatureVariance L r)
    (U : SourceMode 2 → ℝ) (hU : ∀ m, 0 ≤ U m)
    (hUs : ∀ n : ℕ, Summable (fun m => orderModeBound n 2 L m * U m))
    (hχU : ∀ m, |curvatureDirection L r m| ≤ U m)
    (n : ℕ) (M : ℝ)
    (hRint : Integrable (fun η => sourceGammaRadius L η^n) (sourceSmoothKernel hL r p))
    (hRbound : (∫ η, sourceGammaRadius L η^n ∂sourceSmoothKernel hL r p) ≤ M) :
    Integrable (fun ρ => allTargetCurvatureResidualRadius hL r p ρ^n) (curvatureResidualLaw hL r) ∧
      (∫ ρ, allTargetCurvatureResidualRadius hL r p ρ^n ∂curvatureResidualLaw hL r) ≤
        (2:ℝ)^(n-1)*(M + curvatureEnvelopeTotal L U^n*standardAbsMoment n) := by
  let Φ := posteriorSample hL r p
  let μ := smoothLaw 2 L
  let H := curvatureEnvelopeTotal L U
  have hH : 0 ≤ H := curvatureEnvelopeTotal_nonneg L U hU
  have hΦmeas : Measurable Φ :=
    (posteriorSample_measurable hL r).comp (measurable_const.prodMk measurable_id)
  have hΦlaw : HasLaw Φ (sourceSmoothKernel hL r p) μ := by
    refine ⟨hΦmeas.aemeasurable,?_⟩
    rw [sourceSmoothKernel_apply]
  have hRfint : Integrable (fun ω => sourceGammaRadius L (Φ ω)^n) μ := hΦlaw.integrable_comp hRint
  have hRfbound : (∫ ω, sourceGammaRadius L (Φ ω)^n ∂μ) ≤ M :=
    (hΦlaw.integral_comp ((sourceGammaRadius_measurable L).pow_const n).aestronglyMeasurable).trans_le hRbound
  have hZlaw := curvatureZ_hasLaw hL r hG hτ
  have hZint : Integrable (fun ω => |curvatureZ L r ω|^n) μ :=
    hZlaw.integrable_comp (standardAbsMoment_integrable n)
  have hZeq : (∫ ω, |curvatureZ L r ω|^n ∂μ) = standardAbsMoment n :=
    hZlaw.integral_comp (show AEStronglyMeasurable (fun z : ℝ => |z|^n) (gaussianReal 0 1) by fun_prop)
  have hmajor : Integrable (fun ω => (2:ℝ)^(n-1)*
      (sourceGammaRadius L (Φ ω)^n + H^n*|curvatureZ L r ω|^n)) μ :=
    (hRfint.add (hZint.const_mul _)).const_mul _
  have hpoint (ω : SmoothSample 2 L) : allTargetCurvatureResidualRadius hL r p (curvatureResidualSample hL r ω)^n ≤
      (2:ℝ)^(n-1)*(sourceGammaRadius L (Φ ω)^n + H^n*|curvatureZ L r ω|^n) := by
    have hs : 0 ≤ allTargetCurvatureResidualRadius hL r p (curvatureResidualSample hL r ω) :=
      (by norm_num : (0:ℝ) ≤ 1).trans (one_le_allTargetCurvatureResidualRadius hL r p _)
    calc
      _ ≤ (sourceGammaRadius L (Φ ω)+H*|curvatureZ L r ω|)^n :=
        pow_le_pow_left₀ hs (allTargetCurvatureResidualRadius_image_bound hL r p hG U hU hUs hχU ω) n
      _ ≤ (2:ℝ)^(n-1)*(sourceGammaRadius L (Φ ω)^n+(H*|curvatureZ L r ω|)^n) :=
        add_pow_le (sourceGammaRadius_nonneg L _) (mul_nonneg hH (abs_nonneg _)) n
      _ = _ := by rw [mul_pow]
  have himage : Integrable (fun ω => allTargetCurvatureResidualRadius hL r p (curvatureResidualSample hL r ω)^n) μ := by
    apply hmajor.mono'
      ((((allTargetCurvatureResidualRadius_measurable hL r p).comp (curvatureResidualSample_measurable hL r)).pow_const n).aestronglyMeasurable)
    filter_upwards [] with ω
    simp only [Function.comp_apply]
    rw [Real.norm_eq_abs,abs_of_nonneg (pow_nonneg
      ((by norm_num : (0:ℝ) ≤ 1).trans (one_le_allTargetCurvatureResidualRadius hL r p _)) n)]
    exact hpoint ω
  have hint : Integrable (fun ρ => allTargetCurvatureResidualRadius hL r p ρ^n) (curvatureResidualLaw hL r) := by
    exact (integrable_map_measure ((allTargetCurvatureResidualRadius_measurable hL r p).pow_const n).aestronglyMeasurable
      (curvatureResidualSample_measurable hL r).aemeasurable).mpr himage
  refine ⟨hint,?_⟩
  calc
    _ = ∫ ω, allTargetCurvatureResidualRadius hL r p (curvatureResidualSample hL r ω)^n ∂μ :=
      integral_map (curvatureResidualSample_measurable hL r).aemeasurable
        ((allTargetCurvatureResidualRadius_measurable hL r p).pow_const n).aestronglyMeasurable
    _ ≤ ∫ ω, (2:ℝ)^(n-1)*(sourceGammaRadius L (Φ ω)^n+H^n*|curvatureZ L r ω|^n) ∂μ :=
      integral_mono himage hmajor hpoint
    _ = (2:ℝ)^(n-1)*((∫ ω, sourceGammaRadius L (Φ ω)^n ∂μ)+H^n*standardAbsMoment n) := by
      rw [integral_const_mul,integral_add hRfint (hZint.const_mul _),integral_const_mul,hZeq]
    _ ≤ _ := mul_le_mul_of_nonneg_left (add_le_add hRfbound le_rfl) (by positivity)

/-- Exact specialization to the retained default-radius definition. -/
theorem allTargetCurvatureResidualRadius_prescribed {L : ℝ} (hL : L ≠ 0)
    (r b : ℝ) (ρ : SmoothSample 2 L) :
    allTargetCurvatureResidualRadius hL r (sourcePrescribedPins r b) ρ =
      curvatureResidualRadius hL r b ρ := rfl

/-- A single interval and fixed reconstruction/image constants, chosen from hL
alone, work for all targets and all natural moments under the actual residual law.
The covariance inverse, positive variance and summable envelope are internal. -/
theorem allTargetCurvatureResidualRadius_uniform_bounds {L : ℝ} (hL : L ≠ 0) :
    ∃ δ A H : ℝ, 0 < δ ∧ δ ≤ 1 ∧ 0 ≤ A ∧ 0 ≤ H ∧
      (∀ r : ℝ, 0 < r → r < δ → ∀ (p : Fin 6 → ℝ) (ρ : SmoothSample 2 L) (q : ℝ),
        sourceGammaRadius L (curvatureReconstruct hL r p ρ q) ≤
          A*(|q|+allTargetCurvatureResidualRadius hL r p ρ)) ∧
      (∀ r : ℝ, 0 < r → r < δ → ∀ (p : Fin 6 → ℝ) (ω : SmoothSample 2 L),
        allTargetCurvatureResidualRadius hL r p (curvatureResidualSample hL r ω) ≤
          sourceGammaRadius L (posteriorSample hL r p ω) + H*|curvatureZ L r ω|) ∧
      ∀ n : ℕ, ∃ C : ℝ, 0 ≤ C ∧ ∀ r : ℝ, 0 < r → r < δ → ∀ p : Fin 6 → ℝ,
        Integrable (fun ρ => allTargetCurvatureResidualRadius hL r p ρ^n)
          (curvatureResidualLaw hL r) ∧
          (∫ ρ, allTargetCurvatureResidualRadius hL r p ρ^n ∂curvatureResidualLaw hL r) ≤
            C*(1+‖p‖)^n := by
  obtain ⟨δU,hδU,hδU1,U,hU,_hUsum,hUs,hUE⟩ := curvatureDirection_uniform_envelope hL 0
  obtain ⟨B,Mp,δP,_hB,_hMp,hδP,_hδP1,hparam⟩ := curvature_uniform_parameter_bounds hL 0
  obtain ⟨δR,hδR,_hδR1,hmom⟩ := sourceGammaRadius_allTarget_moments hL
  let δ := min δU (min δP δR)
  let H := curvatureEnvelopeTotal L U
  have hH : 0 ≤ H := curvatureEnvelopeTotal_nonneg L U hU
  have hδ : 0 < δ := lt_min hδU (lt_min hδP hδR)
  have hδ1 : δ ≤ 1 := (min_le_left _ _).trans hδU1
  have hrU (r : ℝ) (hrδ : r < δ) : r < δU := lt_of_lt_of_le hrδ (min_le_left _ _)
  have hrP (r : ℝ) (hrδ : r < δ) : r < δP :=
    lt_of_lt_of_le hrδ ((min_le_right _ _).trans (min_le_left _ _))
  have hrR (r : ℝ) (hrδ : r < δ) : r < δR :=
    lt_of_lt_of_le hrδ ((min_le_right _ _).trans (min_le_right _ _))
  have hG (r : ℝ) (hr : 0 < r) (hrδ : r < δ) : IsUnit (sourcePinCovarianceAt L r) :=
    (hparam r hr (hrP r hrδ)).1
  have hτ (r : ℝ) (hr : 0 < r) (hrδ : r < δ) : 0 < curvatureVariance L r :=
    lt_of_lt_of_le (half_pos (sourceContactSchur_pos hL)) (hparam r hr (hrP r hrδ)).2.1
  refine ⟨δ,1+H,H,hδ,hδ1,by positivity,hH,?_,?_,?_⟩
  · intro r hr hrδ p ρ q
    exact sourceGammaRadius_allTarget_curvatureReconstruct hL r p q
      (Real.sqrt_pos.mpr (hτ r hr hrδ)) U hU hUs
      (fun m => (hUE r hr (hrU r hrδ) m).2) ρ
  · intro r hr hrδ p ω
    exact allTargetCurvatureResidualRadius_image_bound hL r p (hG r hr hrδ) U hU hUs
      (fun m => (hUE r hr (hrU r hrδ) m).1) ω
  · intro n
    obtain ⟨M,hM,hRm⟩ := hmom n
    have hstd : 0 ≤ standardAbsMoment n := integral_nonneg (fun z => pow_nonneg (abs_nonneg z) n)
    refine ⟨(2:ℝ)^(n-1)*(M+H^n*standardAbsMoment n),by positivity,?_⟩
    intro r hr hrδ p
    obtain ⟨hRi,hRb⟩ := hRm r hr (hrR r hrδ) p
    obtain ⟨hint,hbound⟩ := allTargetCurvatureResidualRadius_moment_bound hL r p
      (hG r hr hrδ) (hτ r hr hrδ) U hU hUs
      (fun m => (hUE r hr (hrU r hrδ) m).1) n (M*(1+‖p‖)^n) hRi hRb
    refine ⟨hint,hbound.trans ?_⟩
    have hp : (1:ℝ) ≤ (1+‖p‖)^n := one_le_pow₀ (by linarith [norm_nonneg p])
    have hterm : 0 ≤ H^n*standardAbsMoment n := mul_nonneg (pow_nonneg hH n) hstd
    nlinarith [mul_le_mul_of_nonneg_left hp hterm,
      mul_nonneg (by positivity : 0 ≤ (2:ℝ)^(n-1))
        (sub_nonneg.mpr (mul_le_mul_of_nonneg_left hp hterm))]

/-- Bounded literal cubic gap marks give polynomial height growth under the
residual law on the same interval, independent of b,k,n and even of K. -/
theorem allTargetCurvatureResidualRadius_gap_height_moments {L : ℝ} (hL : L ≠ 0) :
    ∃ δ : ℝ, 0 < δ ∧ δ ≤ 1 ∧ ∀ K : ℝ, 0 ≤ K → ∀ n : ℕ,
      ∃ C : ℝ, 0 ≤ C ∧ ∀ r : ℝ, 0 < r → r < δ → ∀ b k : ℝ, |k| ≤ K →
        Integrable (fun ρ => allTargetCurvatureResidualRadius hL r (sourceGapPins r b k) ρ^n)
          (curvatureResidualLaw hL r) ∧
        (∫ ρ, allTargetCurvatureResidualRadius hL r (sourceGapPins r b k) ρ^n
          ∂curvatureResidualLaw hL r) ≤ C*(1+|b|)^n := by
  obtain ⟨δ,A,H,hδ,hδ1,_hA,_hH,_hrec,_himage,hmom⟩ :=
    allTargetCurvatureResidualRadius_uniform_bounds hL
  refine ⟨δ,hδ,hδ1,?_⟩
  intro K hK n
  obtain ⟨C,hC,hbound⟩ := hmom n
  refine ⟨C*(1+13*K)^n,by positivity,?_⟩
  intro r hr hrδ b k hk
  obtain ⟨hint,hb⟩ := hbound r hr hrδ (sourceGapPins r b k)
  refine ⟨hint,hb.trans ?_⟩
  have hp := sourceGapPins_norm_le r b k K hr.le (hrδ.le.trans hδ1) hK hk
  have ht : 1+‖sourceGapPins r b k‖ ≤ (1+13*K)*(1+|b|) := by
    nlinarith [mul_nonneg hK (abs_nonneg b)]
  calc
    _ ≤ C*((1+13*K)*(1+|b|))^n :=
      mul_le_mul_of_nonneg_left (pow_le_pow_left₀ (by positivity) ht n) hC
    _ = _ := by rw [mul_pow]; ring

end I4SourceAllTargetCurvatureResidual
