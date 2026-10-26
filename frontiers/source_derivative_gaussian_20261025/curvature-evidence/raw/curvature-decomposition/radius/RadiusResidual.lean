import SourceCurvatureDecomposition
import SourcePinCurvatureBounds

noncomputable section
open I4Foundation I4Source I4Smooth I4SmoothCarrier I4SourceGaussian I4SourceCovariance
open I4SourceDerivativeGaussian I4SourceDerivativeContinuity I4SourceConfluentPins
open I4SourceConfluentLimits I4ContactCoefficientLimits I4SourceEndpointRegression
open I4SourceContact I4SourceSmoothConditional I4SourceConditionalMajorant I4ContactGram
open I4GaussianRegressionLimits I4SourceEndpointEstimates I4SourceSmoothPalm
open I4SourcePinCurvatureBounds I4GaussianMajorant MeasureTheory ProbabilityTheory Matrix Filter
open scoped BigOperators Topology NNReal
set_option autoImplicit false
namespace I4SourceCurvatureDecomposition

def curvatureResidualRadius {L : ℝ} (hL : L ≠ 0) (r b : ℝ) (ρ : SmoothSample 2 L) : ℝ :=
  sourceGammaRadius L (posteriorSample hL r (sourcePrescribedPins r b) ρ)

theorem curvatureResidualRadius_measurable {L : ℝ} (hL : L ≠ 0) (r b : ℝ) :
    Measurable (curvatureResidualRadius hL r b) :=
  (sourceGammaRadius_measurable L).comp
    ((posteriorSample_measurable hL r).comp (measurable_const.prodMk measurable_id))

theorem one_le_curvatureResidualRadius {L : ℝ} (hL : L ≠ 0) (r b : ℝ) (ρ : SmoothSample 2 L) :
    1 ≤ curvatureResidualRadius hL r b ρ := one_le_sourceGammaRadius L _

theorem sourceContactQ_posterior_abs_le_radius {L : ℝ} (hL : L ≠ 0) (r b : ℝ)
    (ρ : SmoothSample 2 L) :
    |sourceContactQ L (posteriorSample hL r (sourcePrescribedPins r b) ρ)| ≤ curvatureResidualRadius hL r b ρ := by
  exact (sourceQ_abs_le hL _).trans (sourceDerivativeMajorant_le_radius L _ (2 : Fin 6))

def curvatureEnvelopeTotal (L : ℝ) (U : SourceMode 2 → ℝ) : ℝ :=
  ∑ k : Fin 6, ∑' m, orderModeBound k 2 L m * U m

theorem curvatureEnvelopeTotal_nonneg (L : ℝ) (U : SourceMode 2 → ℝ) (hU : ∀ m, 0 ≤ U m) :
    0 ≤ curvatureEnvelopeTotal L U :=
  Finset.sum_nonneg (fun k _ => tsum_nonneg (fun m => mul_nonneg (orderModeBound_nonneg k 2 L m) (hU m)))

theorem sourceDerivativeMajorant_curvatureShift {L : ℝ} (hL : L ≠ 0) (r t : ℝ)
    (k : ℕ) (ω : SmoothSample 2 L) :
    sourceDerivativeMajorant L k (curvatureShift hL r t ω) ≤
      sourceDerivativeMajorant L k ω +
        (∑' m, orderModeBound k 2 L m * |curvatureDirection L r m|)*|t| := by
  have hχ := (curvatureDirection_goodSample hL r) k
  have hbase := ω.property k
  have hs := hbase.add (hχ.mul_right |t|)
  have hleft := (curvatureShift hL r t ω).property k
  have hi (m : SourceMode 2) :
      orderModeBound k 2 L m * |(curvatureShift hL r t ω).val m| ≤
      orderModeBound k 2 L m * |ω.val m| +
        (orderModeBound k 2 L m * |curvatureDirection L r m|)*|t| := by
    rw [curvatureShift_val]
    calc
      _ ≤ orderModeBound k 2 L m * (|ω.val m| + |curvatureDirection L r m*t|) :=
        mul_le_mul_of_nonneg_left (abs_add_le _ _) (orderModeBound_nonneg k 2 L m)
      _ = _ := by rw [abs_mul]; ring
  have h := hleft.tsum_le_tsum hi hs
  rw [hbase.tsum_add (hχ.mul_right |t|), tsum_mul_right] at h
  exact h

theorem sourceGammaRadius_curvatureShift {L : ℝ} (hL : L ≠ 0) (r t : ℝ)
    (U : SourceMode 2 → ℝ) (_hU : ∀ m, 0 ≤ U m)
    (hUs : ∀ n : ℕ, Summable (fun m => orderModeBound n 2 L m * U m))
    (hχU : ∀ m, |curvatureDirection L r m| ≤ U m)
    (ω : SmoothSample 2 L) :
    sourceGammaRadius L (curvatureShift hL r t ω) ≤
      sourceGammaRadius L ω + curvatureEnvelopeTotal L U * |t| := by
  have hpart (k : Fin 6) : sourceDerivativeMajorant L k (curvatureShift hL r t ω) ≤
      sourceDerivativeMajorant L k ω + (∑' m, orderModeBound k 2 L m * U m)*|t| := by
    apply (sourceDerivativeMajorant_curvatureShift hL r t k ω).trans
    apply add_le_add le_rfl
    apply mul_le_mul_of_nonneg_right _ (abs_nonneg t)
    exact ((curvatureDirection_goodSample hL r) k).tsum_le_tsum
      (fun m => mul_le_mul_of_nonneg_left (hχU m) (orderModeBound_nonneg k 2 L m)) (hUs k)
  unfold sourceGammaRadius curvatureEnvelopeTotal
  have hs := Finset.sum_le_sum (fun k (_ : k ∈ (Finset.univ : Finset (Fin 6))) => hpart k)
  rw [Finset.sum_add_distrib, ← Finset.sum_mul] at hs
  linarith

theorem sourceDerivativeMajorant_curvatureReconstruct {L : ℝ} (hL : L ≠ 0) (r b q : ℝ)
    (hσ : 0 < curvatureSigma L r) (U : SourceMode 2 → ℝ)
    (hU : ∀ m, 0 ≤ U m)
    (hUs : ∀ n : ℕ, Summable (fun m => orderModeBound n 2 L m * U m))
    (hχU : ∀ m, |curvatureDirection L r m|/curvatureSigma L r ≤ U m)
    (k : ℕ) (ρ : SmoothSample 2 L) :
    sourceDerivativeMajorant L k
      (curvatureReconstruct hL r (sourcePrescribedPins r b) ρ q) ≤
      sourceDerivativeMajorant L k (posteriorSample hL r (sourcePrescribedPins r b) ρ) +
        (∑' m, orderModeBound k 2 L m*U m)*(|q|+curvatureResidualRadius hL r b ρ) := by
  let φ := posteriorSample hL r (sourcePrescribedPins r b) ρ
  have hbase := φ.property k
  have hright := hbase.add ((hUs k).mul_right (|q|+curvatureResidualRadius hL r b ρ))
  have hleft := (curvatureReconstruct hL r (sourcePrescribedPins r b) ρ q).property k
  have hq : |q-sourceContactQ L φ| ≤ |q|+curvatureResidualRadius hL r b ρ := by
    exact (abs_sub _ _).trans (add_le_add le_rfl (sourceContactQ_posterior_abs_le_radius hL r b ρ))
  have ht0 : 0 ≤ |q|+curvatureResidualRadius hL r b ρ := by
    have hs := one_le_curvatureResidualRadius hL r b ρ
    linarith [abs_nonneg q]
  have hi (m : SourceMode 2) :
      orderModeBound k 2 L m * |(curvatureReconstruct hL r (sourcePrescribedPins r b) ρ q).val m| ≤
      orderModeBound k 2 L m * |φ.val m| +
        (orderModeBound k 2 L m*U m)*(|q|+curvatureResidualRadius hL r b ρ) := by
    change orderModeBound k 2 L m * |φ.val m + curvatureDirection L r m *
      ((q-sourceContactQ L φ)/curvatureSigma L r)| ≤ _
    have hshift : |curvatureDirection L r m * ((q-sourceContactQ L φ)/curvatureSigma L r)| ≤
        U m*(|q|+curvatureResidualRadius hL r b ρ) := by
      rw [abs_mul, abs_div, abs_of_pos hσ]
      have heq : |curvatureDirection L r m| * (|q-sourceContactQ L φ|/curvatureSigma L r) =
          (|curvatureDirection L r m|/curvatureSigma L r)*|q-sourceContactQ L φ| := by ring
      rw [heq]
      exact mul_le_mul (hχU m) hq (abs_nonneg _) (hU m)
    calc
      _ ≤ orderModeBound k 2 L m * (|φ.val m| +
          |curvatureDirection L r m * ((q-sourceContactQ L φ)/curvatureSigma L r)|) :=
        mul_le_mul_of_nonneg_left (abs_add_le _ _) (orderModeBound_nonneg k 2 L m)
      _ ≤ orderModeBound k 2 L m * (|φ.val m|+U m*(|q|+curvatureResidualRadius hL r b ρ)) :=
        mul_le_mul_of_nonneg_left (add_le_add le_rfl hshift) (orderModeBound_nonneg k 2 L m)
      _ = _ := by ring
  have h := hleft.tsum_le_tsum hi hright
  rw [hbase.tsum_add ((hUs k).mul_right _), tsum_mul_right] at h
  exact h

theorem sourceGammaRadius_curvatureReconstruct {L : ℝ} (hL : L ≠ 0) (r b q : ℝ)
    (hσ : 0 < curvatureSigma L r) (U : SourceMode 2 → ℝ)
    (hU : ∀ m, 0 ≤ U m)
    (hUs : ∀ n : ℕ, Summable (fun m => orderModeBound n 2 L m * U m))
    (hχU : ∀ m, |curvatureDirection L r m|/curvatureSigma L r ≤ U m)
    (ρ : SmoothSample 2 L) :
    sourceGammaRadius L (curvatureReconstruct hL r (sourcePrescribedPins r b) ρ q) ≤
      (1+curvatureEnvelopeTotal L U)*(|q|+curvatureResidualRadius hL r b ρ) := by
  have hpart (k : Fin 6) := sourceDerivativeMajorant_curvatureReconstruct hL r b q hσ U hU hUs hχU k ρ
  have hs := Finset.sum_le_sum (fun k (_ : k ∈ (Finset.univ : Finset (Fin 6))) => hpart k)
  rw [Finset.sum_add_distrib, ← Finset.sum_mul] at hs
  change 1+∑ k : Fin 6, sourceDerivativeMajorant L k
      (curvatureReconstruct hL r (sourcePrescribedPins r b) ρ q) ≤ _
  dsimp [curvatureResidualRadius, sourceGammaRadius, curvatureEnvelopeTotal] at *
  nlinarith [abs_nonneg q]

theorem curvaturePosterior_residual_eq_shift {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (hG : IsUnit (sourcePinCovarianceAt L r)) (x : Fin 6 → ℝ) (ω : SmoothSample 2 L) :
    posteriorSample hL r x (curvatureResidualSample hL r ω) =
      curvatureShift hL r (-curvatureZ L r ω) (posteriorSample hL r x ω) := by
  apply Subtype.ext
  funext m
  have h := congrArg (fun η : SmoothSample 2 L => η.val m)
    (curvaturePosterior_reconstruction hL r hG x ω)
  simp only [curvatureShift_val] at h ⊢
  linarith

theorem curvatureResidualRadius_image_bound {L : ℝ} (hL : L ≠ 0) (r b : ℝ)
    (hG : IsUnit (sourcePinCovarianceAt L r)) (U : SourceMode 2 → ℝ)
    (hU : ∀ m, 0 ≤ U m)
    (hUs : ∀ n : ℕ, Summable (fun m => orderModeBound n 2 L m * U m))
    (hχU : ∀ m, |curvatureDirection L r m| ≤ U m) (ω : SmoothSample 2 L) :
    curvatureResidualRadius hL r b (curvatureResidualSample hL r ω) ≤
      sourceGammaRadius L (posteriorSample hL r (sourcePrescribedPins r b) ω) +
        curvatureEnvelopeTotal L U * |curvatureZ L r ω| := by
  unfold curvatureResidualRadius
  rw [curvaturePosterior_residual_eq_shift hL r hG]
  simpa only [abs_neg] using sourceGammaRadius_curvatureShift hL r (-curvatureZ L r ω)
    U hU hUs hχU (posteriorSample hL r (sourcePrescribedPins r b) ω)

theorem curvatureResidualRadius_moment_bound {L : ℝ} (hL : L ≠ 0) (r b : ℝ)
    (hG : IsUnit (sourcePinCovarianceAt L r)) (hτ : 0 < curvatureVariance L r)
    (U : SourceMode 2 → ℝ) (hU : ∀ m, 0 ≤ U m)
    (hUs : ∀ n : ℕ, Summable (fun m => orderModeBound n 2 L m * U m))
    (hχU : ∀ m, |curvatureDirection L r m| ≤ U m)
    (n : ℕ) (M : ℝ)
    (hRint : Integrable (fun η => sourceGammaRadius L η^n) (sourceSmoothLaw hL r b))
    (hRbound : (∫ η, sourceGammaRadius L η^n ∂sourceSmoothLaw hL r b) ≤ M) :
    Integrable (fun ρ => curvatureResidualRadius hL r b ρ^n) (curvatureResidualLaw hL r) ∧
      (∫ ρ, curvatureResidualRadius hL r b ρ^n ∂curvatureResidualLaw hL r) ≤
        (2:ℝ)^(n-1)*(M + curvatureEnvelopeTotal L U^n*standardAbsMoment n) := by
  let Φ := posteriorSample hL r (sourcePrescribedPins r b)
  let μ := smoothLaw 2 L
  let H := curvatureEnvelopeTotal L U
  have hH : 0 ≤ H := curvatureEnvelopeTotal_nonneg L U hU
  have hΦmeas : Measurable Φ :=
    (posteriorSample_measurable hL r).comp (measurable_const.prodMk measurable_id)
  have hΦlaw : HasLaw Φ (sourceSmoothLaw hL r b) μ := by
    refine ⟨hΦmeas.aemeasurable,?_⟩
    rw [sourceSmoothLaw,sourceSmoothKernel_apply]
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
  have hpoint (ω : SmoothSample 2 L) : curvatureResidualRadius hL r b (curvatureResidualSample hL r ω)^n ≤
      (2:ℝ)^(n-1)*(sourceGammaRadius L (Φ ω)^n + H^n*|curvatureZ L r ω|^n) := by
    have hs : 0 ≤ curvatureResidualRadius hL r b (curvatureResidualSample hL r ω) :=
      (by norm_num : (0:ℝ) ≤ 1).trans (one_le_curvatureResidualRadius hL r b _)
    calc
      _ ≤ (sourceGammaRadius L (Φ ω)+H*|curvatureZ L r ω|)^n :=
        pow_le_pow_left₀ hs (curvatureResidualRadius_image_bound hL r b hG U hU hUs hχU ω) n
      _ ≤ (2:ℝ)^(n-1)*(sourceGammaRadius L (Φ ω)^n+(H*|curvatureZ L r ω|)^n) :=
        add_pow_le (sourceGammaRadius_nonneg L _) (mul_nonneg hH (abs_nonneg _)) n
      _ = _ := by rw [mul_pow]
  have himage : Integrable (fun ω => curvatureResidualRadius hL r b (curvatureResidualSample hL r ω)^n) μ := by
    apply hmajor.mono'
      ((((curvatureResidualRadius_measurable hL r b).comp (curvatureResidualSample_measurable hL r)).pow_const n).aestronglyMeasurable)
    filter_upwards [] with ω
    simp only [Function.comp_apply]
    rw [Real.norm_eq_abs,abs_of_nonneg (pow_nonneg
      ((by norm_num : (0:ℝ) ≤ 1).trans (one_le_curvatureResidualRadius hL r b _)) n)]
    exact hpoint ω
  have hint : Integrable (fun ρ => curvatureResidualRadius hL r b ρ^n) (curvatureResidualLaw hL r) := by
    exact (integrable_map_measure ((curvatureResidualRadius_measurable hL r b).pow_const n).aestronglyMeasurable
      (curvatureResidualSample_measurable hL r).aemeasurable).mpr himage
  refine ⟨hint,?_⟩
  calc
    _ = ∫ ω, curvatureResidualRadius hL r b (curvatureResidualSample hL r ω)^n ∂μ :=
      integral_map (curvatureResidualSample_measurable hL r).aemeasurable
        ((curvatureResidualRadius_measurable hL r b).pow_const n).aestronglyMeasurable
    _ ≤ ∫ ω, (2:ℝ)^(n-1)*(sourceGammaRadius L (Φ ω)^n+H^n*|curvatureZ L r ω|^n) ∂μ :=
      integral_mono himage hmajor hpoint
    _ = (2:ℝ)^(n-1)*((∫ ω, sourceGammaRadius L (Φ ω)^n ∂μ)+H^n*standardAbsMoment n) := by
      rw [integral_const_mul,integral_add hRfint (hZint.const_mul _),integral_const_mul,hZeq]
    _ ≤ _ := mul_le_mul_of_nonneg_left (add_le_add hRfbound le_rfl) (by positivity)

theorem curvatureResidualRadius_uniform_bounds {L : ℝ} (hL : L ≠ 0) (b : ℝ) :
    ∃ δ A H : ℝ, 0 < δ ∧ δ ≤ 1 ∧ 0 ≤ A ∧ 0 ≤ H ∧
      (∀ r : ℝ, 0 < r → r < δ → ∀ (ρ : SmoothSample 2 L) (q : ℝ),
        sourceGammaRadius L (curvatureReconstruct hL r (sourcePrescribedPins r b) ρ q) ≤
          A*(|q|+curvatureResidualRadius hL r b ρ)) ∧
      (∀ r : ℝ, 0 < r → r < δ → ∀ ω : SmoothSample 2 L,
        curvatureResidualRadius hL r b (curvatureResidualSample hL r ω) ≤
          sourceGammaRadius L (posteriorSample hL r (sourcePrescribedPins r b) ω) + H*|curvatureZ L r ω|) ∧
      ∀ n : ℕ, ∃ M : ℝ, 0 ≤ M ∧ ∀ r : ℝ, 0 < r → r < δ →
        Integrable (fun ρ => curvatureResidualRadius hL r b ρ^n) (curvatureResidualLaw hL r) ∧
          (∫ ρ, curvatureResidualRadius hL r b ρ^n ∂curvatureResidualLaw hL r) ≤ M := by
  obtain ⟨δU,hδU,hδU1,U,hU,_hUsum,hUs,hUE⟩ := curvatureDirection_uniform_envelope hL b
  obtain ⟨B,Mp,δP,_hB,_hMp,hδP,_hδP1,hparam⟩ := curvature_uniform_parameter_bounds hL b
  obtain ⟨δR,hδR,_hδR1,hmom⟩ := sourceGammaRadius_moments hL b
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
  · intro r hr hrδ ρ q
    exact sourceGammaRadius_curvatureReconstruct hL r b q (Real.sqrt_pos.mpr (hτ r hr hrδ)) U hU hUs
      (fun m => (hUE r hr (hrU r hrδ) m).2) ρ
  · intro r hr hrδ ω
    exact curvatureResidualRadius_image_bound hL r b (hG r hr hrδ) U hU hUs
      (fun m => (hUE r hr (hrU r hrδ) m).1) ω
  · intro n
    obtain ⟨M,hM,hRm⟩ := hmom n
    have hstd : 0 ≤ standardAbsMoment n := integral_nonneg (fun z => pow_nonneg (abs_nonneg z) n)
    refine ⟨(2:ℝ)^(n-1)*(M+H^n*standardAbsMoment n),by positivity,?_⟩
    intro r hr hrδ
    obtain ⟨hRi,hRb⟩ := hRm r hr (hrR r hrδ)
    exact curvatureResidualRadius_moment_bound hL r b (hG r hr hrδ) (hτ r hr hrδ) U hU hUs
      (fun m => (hUE r hr (hrU r hrδ) m).1) n M hRi hRb
end I4SourceCurvatureDecomposition
