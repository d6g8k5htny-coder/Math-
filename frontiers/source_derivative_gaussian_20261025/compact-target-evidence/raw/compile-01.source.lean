import SourcePinCurvatureBounds
import SourceRawPinConditioning

/-!
# Actual source moments at every target

One interval, depending only on the actual nonzero period, works for every
six-dimensional target and every natural moment. The original Gaussian sample
law and its summable Fourier weights are retained throughout. Varying cubic
gaps use their literal confluent targets and the every-target raw sampling lift.
These are unweighted moment statements, with no geometric or Palm conclusion.
-/

noncomputable section

open I4Foundation I4Source I4Weights I4Smooth I4SmoothCarrier
open I4SourceDerivativeGaussian I4SourceConfluentPins I4SourceConfluentLimits
open I4SourceEndpointRegression I4SourceEndpointEstimates I4SourceSmoothConditional
open I4SourceConditionalMajorant I4SourcePinCurvatureBounds I4SourceSmoothPalm
open I4SourceRawPinConditioning MeasureTheory ProbabilityTheory Filter
open scoped BigOperators Topology Matrix

set_option autoImplicit false

namespace I4SourceCompactTargetMoments

/-- Actual inverse bounds and actual invertibility on one target-independent interval. -/
theorem sourceInverse_target_uniform_bounds {L : ℝ} (hL : L ≠ 0) :
    ∃ K δ : ℝ, 0 ≤ K ∧ 0 < δ ∧ δ ≤ 1 ∧
      ∀ r : ℝ, 0 < r → r < δ →
        IsUnit (sourcePinCovarianceAt L r) ∧
        ∀ i j, |(sourcePinCovarianceAt L r)⁻¹ i j| ≤ K := by
  obtain ⟨K, D, δ, hK, _hD, hδ, hδ1, hb⟩ :=
    sourceInverse_prescribed_uniform_bounds hL 0
  obtain ⟨ε, hε, hu⟩ := mem_nhdsGT_iff_exists_Ioo_subset.mp
    (sourceEndpoint_parameter_limits hL 0).1
  refine ⟨K, min δ ε, hK, lt_min hδ hε,
    (min_le_left _ _).trans hδ1, ?_⟩
  intro r hr hrδ
  exact ⟨hu ⟨hr, hrδ.trans_le (min_le_right _ _)⟩,
    (hb r hr (hrδ.trans_le (min_le_left _ _))).1⟩

/-- A fixed nonnegative summable weight on the original coefficients controls
the posterior radius at every target, with its full linear target dependence. -/
theorem sourceGammaRadius_allTarget_domination {L : ℝ} (hL : L ≠ 0) :
    ∃ a : ℝ, ∃ w : SourceMode 2 → ℝ, ∃ δ : ℝ,
      0 ≤ a ∧ (∀ m, 0 ≤ w m) ∧ Summable w ∧ 0 < δ ∧ δ ≤ 1 ∧
      ∀ r : ℝ, 0 < r → r < δ → ∀ p : Fin 6 → ℝ, ∀ ω : SmoothSample 2 L,
        sourceGammaRadius L (posteriorSample hL r p ω) ≤
          (1 + ‖p‖) * (a + sampleMajorant w ω) := by
  obtain ⟨K, δ, hK, hδ, hδ1, hb⟩ := sourceInverse_target_uniform_bounds hL
  let w0 := orderModeBound 5 2 L
  let A := confluentModeMajorant L
  have hw0 : ∀ m, 0 ≤ w0 m := orderModeBound_nonneg 5 2 L
  have hA : ∀ m, 0 ≤ A m := confluentModeMajorant_nonneg L
  have hwA : Summable (fun m => w0 m * A m) := coefficient_product_summable
    (orderModeBound_summable 5 2 hL) (confluentModeMajorant_summable hL)
  let C := 36 * K * (∑' m, w0 m * A m)
  have hC : 0 ≤ C := mul_nonneg (mul_nonneg (by norm_num) hK)
    (tsum_nonneg (fun m => mul_nonneg (hw0 m) (hA m)))
  let v := fun m => w0 m + C * A m
  let w := fun m => 6 * v m
  have hv : Summable v := (orderModeBound_summable 5 2 hL).add
    ((confluentModeMajorant_summable hL).mul_left C)
  have hv0 : ∀ m, 0 ≤ v m := fun m => add_nonneg (hw0 m) (mul_nonneg hC (hA m))
  have hw : Summable w := hv.mul_left 6
  have hwpos : ∀ m, 0 ≤ w m := fun m => mul_nonneg (by norm_num) (hv0 m)
  refine ⟨1 + 6*C, w, δ, by positivity, hwpos, hw, hδ, hδ1, ?_⟩
  intro r hr hrδ p ω
  have hp : ∀ i, |p i| ≤ ‖p‖ := fun i => by
    simpa only [Real.norm_eq_abs] using norm_le_pi_norm p i
  have hd := (posterior_sampleMajorant_le hL r hr.ne' w0 hw0 hwA K ‖p‖ hK
    (norm_nonneg p) (hb r hr hrδ).2 p hp ω (ω.property 5)).2
  have hrec : sampleMajorant w ω =
      6 * (sampleMajorant w0 ω + C * sampleMajorant A ω) := by
    rw [show w = (fun m => 6 * v m) from rfl, sampleMajorant_const_mul]
    rw [show v = (fun m => w0 m + C*A m) from rfl,
      sampleMajorant_add w0 (fun m => C*A m) ω (ω.property 5)]
    · rw [sampleMajorant_const_mul]
    · convert (confluentMajorant_weighted_summable ω).mul_left C using 1
      funext m
      ring
  have hΓ := sourceGammaRadius_le_fifth L (posteriorSample hL r p ω)
  change sampleMajorant w0 (posteriorSample hL r p ω) ≤
    sampleMajorant w0 ω + C * (‖p‖ + sampleMajorant A ω) at hd
  change sourceGammaRadius L (posteriorSample hL r p ω) ≤
    1 + 6 * sampleMajorant w0 (posteriorSample hL r p ω) at hΓ
  have hwω := sampleMajorant_nonneg w hwpos ω
  have hp0 := norm_nonneg p
  nlinarith [mul_nonneg hp0 hwω]

/-- Every affine original-sample majorant has every natural Gaussian moment. -/
theorem sampleMajorant_affine_integrable_pow {L : ℝ} (hL : L ≠ 0)
    (a : ℝ) (ha : 0 ≤ a) (w : SourceMode 2 → ℝ)
    (hw0 : ∀ m, 0 ≤ w m) (hw : Summable w) (n : ℕ) :
    Integrable (fun ω : SmoothSample 2 L => (a + sampleMajorant w ω)^n)
      (smoothLaw 2 L) := by
  have : IsProbabilityMeasure (smoothLaw 2 L) := smoothLaw_isProbabilityMeasure 2 hL
  have hΓ := (sampleMajorant_prior_moment hL w hw0 hw n).1
  have hm : Integrable (fun ω : SmoothSample 2 L =>
      (2:ℝ)^(n-1)*(a^n+sampleMajorant w ω^n)) (smoothLaw 2 L) :=
    ((integrable_const _).add hΓ).const_mul _
  apply hm.mono' (((sampleMajorant_measurable L w).const_add a).pow_const n).aestronglyMeasurable
  filter_upwards [] with ω
  rw [Real.norm_eq_abs, abs_of_nonneg (pow_nonneg
    (add_nonneg ha (sampleMajorant_nonneg w hw0 ω)) n)]
  exact add_pow_le ha (sampleMajorant_nonneg w hw0 ω) n

/-- One positive interval works simultaneously for all literal targets and all
natural moments; no moment or invertibility estimate is an input premise. -/
theorem sourceGammaRadius_allTarget_moments {L : ℝ} (hL : L ≠ 0) :
    ∃ δ : ℝ, 0 < δ ∧ δ ≤ 1 ∧ ∀ n : ℕ, ∃ C : ℝ, 0 ≤ C ∧
      ∀ r : ℝ, 0 < r → r < δ → ∀ p : Fin 6 → ℝ,
        Integrable (fun ω => sourceGammaRadius L ω ^ n) (sourceSmoothKernel hL r p) ∧
        (∫ ω, sourceGammaRadius L ω ^ n ∂sourceSmoothKernel hL r p) ≤
          C * (1 + ‖p‖)^n := by
  obtain ⟨a,w,δ,ha,hw0,hw,hδ,hδ1,hdom⟩ := sourceGammaRadius_allTarget_domination hL
  refine ⟨δ,hδ,hδ1,?_⟩
  intro n
  let F : SmoothSample 2 L → ℝ := fun ω => (a + sampleMajorant w ω)^n
  have hF : Integrable F (smoothLaw 2 L) :=
    sampleMajorant_affine_integrable_pow hL a ha w hw0 hw n
  have hF0 : ∀ ω, 0 ≤ F ω := fun ω =>
    pow_nonneg (add_nonneg ha (sampleMajorant_nonneg w hw0 ω)) n
  refine ⟨∫ ω, F ω ∂smoothLaw 2 L, integral_nonneg hF0, ?_⟩
  intro r hr hrδ p
  have hp : Measurable (posteriorSample hL r p) :=
    (posteriorSample_measurable hL r).comp (measurable_const.prodMk measurable_id)
  have hg := (sourceGammaRadius_measurable L).pow_const n
  have hm := hF.const_mul ((1 + ‖p‖)^n)
  have hpoint (ω : SmoothSample 2 L) :
      sourceGammaRadius L (posteriorSample hL r p ω)^n ≤ (1 + ‖p‖)^n * F ω := by
    simpa only [mul_pow] using pow_le_pow_left₀
      (sourceGammaRadius_nonneg L _) (hdom r hr hrδ p ω) n
  have hpost : Integrable (fun ω => sourceGammaRadius L (posteriorSample hL r p ω)^n)
      (smoothLaw 2 L) := by
    apply hm.mono' (hg.comp hp).aestronglyMeasurable
    filter_upwards [] with ω
    rw [Real.norm_eq_abs, abs_of_nonneg (pow_nonneg (sourceGammaRadius_nonneg L _) n)]
    exact hpoint ω
  rw [sourceSmoothKernel_apply hL r p]
  refine ⟨(integrable_map_measure hg.aestronglyMeasurable hp.aemeasurable).mpr hpost, ?_⟩
  rw [integral_map hp.aemeasurable hg.aestronglyMeasurable]
  calc
    _ ≤ ∫ ω, (1 + ‖p‖)^n * F ω ∂smoothLaw 2 L := integral_mono hpost hm hpoint
    _ = _ := by rw [integral_const_mul]; ring

/-- Literal target for a raw height drop k r³. -/
def sourceGapPins (r b k : ℝ) : Fin 6 → ℝ := ![b-k*r^3/2,0,0,0,0,12*k]

/-- The varying-gap law evaluates the actual all-target posterior kernel. -/
def sourceGapLaw {L : ℝ} (hL : L ≠ 0) (r b k : ℝ) : Measure (SmoothSample 2 L) :=
  sourceSmoothKernel hL r (sourceGapPins r b k)

theorem sourceGapPins_one_sixth (r b : ℝ) :
    sourceGapPins r b (1/6) = sourcePrescribedPins r b := by
  ext i
  fin_cases i <;> simp [sourceGapPins, sourcePrescribedPins] <;> ring

theorem sourceGapLaw_one_sixth {L : ℝ} (hL : L ≠ 0) (r b : ℝ) :
    sourceGapLaw hL r b (1/6) = sourceSmoothLaw hL r b := by
  simp only [sourceGapLaw, sourceGapPins_one_sixth, sourceSmoothLaw]

/-- Exact raw/confluent target algebra, retaining the cubic radius factor. -/
theorem sourceGapPins_eq_confluent (r b k : ℝ) (hr : r ≠ 0) :
    confluentTransform r ![b,b-k*r^3,0,0,0,0] = sourceGapPins r b k := by
  ext i
  fin_cases i <;> simp [confluentTransform, sourceGapPins]
  all_goals field_simp
  all_goals ring

/-- Every-target raw sampling transport, with no use of a.e. RCD uniqueness. -/
theorem sourceGapLaw_eq_rawPinKernel {L : ℝ} (hL : L ≠ 0)
    (r b k : ℝ) (hr : r ≠ 0) :
    sourceGapLaw hL r b k = rawPinKernel hL r ![b,b-k*r^3,0,0,0,0] := by
  rw [rawPinKernel_eq_confluent hL r hr, sourceGapPins_eq_confluent r b k hr]
  rfl

theorem sourceGapPins_norm_le (r b k K : ℝ) (hr : 0 ≤ r) (hr1 : r ≤ 1)
    (hK : 0 ≤ K) (hk : |k| ≤ K) :
    ‖sourceGapPins r b k‖ ≤ |b| + 13*K := by
  have hr3 : 0 ≤ r^3 := pow_nonneg hr 3
  have hr31 : r^3 ≤ 1 := by simpa using pow_le_pow_left₀ hr hr1 3
  apply (pi_norm_le_iff_of_nonneg (by positivity : 0 ≤ |b| + 13*K)).mpr
  intro i
  fin_cases i <;> simp only [sourceGapPins, Matrix.cons_val_zero, Matrix.cons_val_succ,
    Real.norm_eq_abs, abs_zero]
  · calc
      _ ≤ |b| + |k*r^3/2| := abs_sub _ _
      _ ≤ |b| + K/2 := by
        rw [abs_div, abs_mul, abs_of_nonneg hr3]
        norm_num
        gcongr
      _ ≤ _ := by linarith
  · positivity
  · positivity
  · positivity
  · positivity
  · rw [abs_mul]
    norm_num
    nlinarith [abs_nonneg b]

/-- For bounded gap coefficient, every height has a polynomial height bound
on one interval independent of height, coefficient, and moment order. -/
theorem sourceGapLaw_height_moments {L : ℝ} (hL : L ≠ 0) (K : ℝ) (hK : 0 ≤ K) :
    ∃ δ : ℝ, 0 < δ ∧ δ ≤ 1 ∧ ∀ n : ℕ, ∃ C : ℝ, 0 ≤ C ∧
      ∀ r : ℝ, 0 < r → r < δ → ∀ b k : ℝ, |k| ≤ K →
        Integrable (fun ω => sourceGammaRadius L ω ^ n) (sourceGapLaw hL r b k) ∧
        (∫ ω, sourceGammaRadius L ω ^ n ∂sourceGapLaw hL r b k) ≤
          C * (1 + |b|)^n := by
  obtain ⟨δ,hδ,hδ1,hm⟩ := sourceGammaRadius_allTarget_moments hL
  refine ⟨δ,hδ,hδ1,?_⟩
  intro n
  obtain ⟨C,hC,hbound⟩ := hm n
  refine ⟨C*(1+13*K)^n, by positivity, ?_⟩
  intro r hr hrδ b k hk
  obtain ⟨hint,hb⟩ := hbound r hr hrδ (sourceGapPins r b k)
  refine ⟨hint, hb.trans ?_⟩
  have hp := sourceGapPins_norm_le r b k K hr.le (hrδ.le.trans hδ1) hK hk
  have ht : 1 + ‖sourceGapPins r b k‖ ≤ (1+13*K)*(1+|b|) := by
    nlinarith [mul_nonneg hK (abs_nonneg b)]
  calc
    _ ≤ C * ((1+13*K)*(1+|b|))^n :=
      mul_le_mul_of_nonneg_left (pow_le_pow_left₀ (by positivity) ht n) hC
    _ = _ := by rw [mul_pow]; ring

end I4SourceCompactTargetMoments
