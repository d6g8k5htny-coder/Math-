import SourceSmoothPalm
import Mathlib.LinearAlgebra.Matrix.ToLin

/-!
# Canonical whole-carrier conditioning on the literal raw six pins

Source: SOURCE_RAW_PIN_CONDITIONING.md, frozen before implementation.
The posterior is the literal raw coefficient covariance lift. Its equality
with the confluent posterior holds for every target and every carrier sample;
no almost-everywhere conditional-version uniqueness is evaluated at a null pin.
The physical weighted law is transported from the qualified source estimates.
This module does not formalize Kac–Rice or define a synthetic geometric count.

OpenAI author-side work by /root/palm_measure_transfer. Coordinate-change
algebra reuses its checked RawConfluentLift.lean scratch companion.
Finite covariance-congruence and nonsingularity helpers coauthored by
/root/regression_kernel in checked scratch CovarianceCongruence.lean.
-/

noncomputable section
open I4Foundation I4Source I4Smooth I4SmoothCarrier I4SourceGaussian I4SourceCovariance
open I4SourceDerivativeGaussian I4SourceConfluentPins I4SourceConfluentLimits
open I4SourceEndpointRegression I4SourceEndpointEstimates I4SourceSmoothConditional
open I4SourceSmoothPalm I4ContactGram ResearchFormalCoreR1 MeasureTheory ProbabilityTheory Matrix Filter
open scoped BigOperators Matrix Topology
set_option autoImplicit false

namespace I4SourceRawPinConditioning

/-- The actual first six rows of the existing twelve-derivative source. -/
def rawPinCoefficient (L r : ℝ) (i : Fin 6) (m : SourceMode 2) : ℝ :=
  rawDerivativeCoefficient L r (Fin.castAdd 6 i) m

theorem rawPinCoefficient_summable {L : ℝ} (hL : L ≠ 0) (r : ℝ) (i : Fin 6) :
    Summable (rawPinCoefficient L r i) :=
  derivativeCoefficient_summable 2 hL (rawDerivativeOrder (Fin.castAdd 6 i))
    (rawDerivativePoint r (Fin.castAdd 6 i)) (rawDerivativeDirections (Fin.castAdd 6 i))

theorem rawPins_series {L : ℝ} (hL : L ≠ 0) (r : ℝ) (ω : SmoothSample 2 L) :
    rawPins L r ω =
      fun i => scalarSeries (rawPinCoefficient L r i) (sampleInclusion 2 L ω) := by
  funext i
  have h := congrFun (rawPinsWithHessians_series hL r ω) (Fin.castAdd 6 i)
  have hfirst : rawPinsWithHessians L r ω (Fin.castAdd 6 i) = rawPins L r ω i := by
    fin_cases i <;> rfl
  exact hfirst.symm.trans h

theorem rawPins_measurable {L : ℝ} (hL : L ≠ 0) (r : ℝ) :
    Measurable (rawPins L r) := by
  have heq : rawPins L r = fun ω i =>
      scalarSeries (rawPinCoefficient L r i) (sampleInclusion 2 L ω) :=
    funext (rawPins_series hL r)
  rw [heq]
  exact Measurable.of_eval (fun i =>
    (scalarSeries_measurable _).comp (sampleInclusion_measurable 2 L))

/-- Literal covariance of the actual raw observation; the Gram identity is proved below. -/
def rawPinCovariance (L r : ℝ) : Matrix (Fin 6) (Fin 6) ℝ :=
  fun i j => covariance (fun ω => rawPins L r ω i)
    (fun ω => rawPins L r ω j) (smoothLaw 2 L)

theorem rawPinCovariance_coefficient {L : ℝ} (hL : L ≠ 0) (r : ℝ) (i j : Fin 6) :
    rawPinCovariance L r i j =
      ∑' m, rawPinCoefficient L r i m * rawPinCoefficient L r j m := by
  unfold rawPinCovariance
  simp_rw [rawPins_series hL]
  rw [covariance_comp_inclusion 2 hL _ _ (scalarSeries_measurable _)
    (scalarSeries_measurable _)]
  exact I4SourceCovariance.scalarSeries_covariance _ _
    (rawPinCoefficient_summable hL r i) (rawPinCoefficient_summable hL r j)

/-- Matrix of the already proved raw-to-confluent continuous linear equivalence. -/
def confluentMatrix (r : ℝ) (hr : r ≠ 0) : Matrix (Fin 6) (Fin 6) ℝ :=
  LinearMap.toMatrix' (confluentEquiv r hr).toLinearEquiv.toLinearMap

theorem confluentMatrix_mulVec (r : ℝ) (hr : r ≠ 0) (v : Fin 6 → ℝ) :
    confluentMatrix r hr *ᵥ v = confluentTransform r v :=
  LinearMap.toMatrix'_mulVec (confluentEquiv r hr).toLinearEquiv.toLinearMap v

theorem confluentMatrix_isUnit (r : ℝ) (hr : r ≠ 0) : IsUnit (confluentMatrix r hr) := by
  apply LinearMap.isUnit_toMatrix'_iff.mpr
  exact (Module.End.isUnit_iff _).mpr (confluentEquiv r hr).bijective

theorem pinCoefficient_eq_confluentMatrix (L r : ℝ) (hr : r ≠ 0) (m : SourceMode 2) :
    (fun i => pinCoefficient L r i m) =
      confluentMatrix r hr *ᵥ (fun i => rawPinCoefficient L r i m) := by
  rw [confluentMatrix_mulVec]
  rfl

theorem sourceConfluentPinsAt_eq_matrix (L r : ℝ) (hr : r ≠ 0)
    (ω : SmoothSample 2 L) :
    sourceConfluentPinsAt L r ω = confluentMatrix r hr *ᵥ rawPins L r ω := by
  rw [confluentMatrix_mulVec]
  rfl

private theorem covariance_matrix_congruence {Ω n m : Type*} [MeasurableSpace Ω]
    [Fintype n] [Fintype m] [DecidableEq n] [DecidableEq m]
    (μ : Measure Ω) [IsFiniteMeasure μ] (X : Ω → n → ℝ)
    (hX : ∀ i, MemLp (fun ω => X ω i) 2 μ) (T : Matrix m n ℝ) :
    (fun i j => covariance (fun ω => (T *ᵥ X ω) i)
      (fun ω => (T *ᵥ X ω) j) μ) =
      T * (Matrix.of fun i j => covariance (fun ω => X ω i) (fun ω => X ω j) μ) * T.transpose := by
  ext i j
  simp only [Matrix.mulVec, dotProduct]
  rw [covariance_fun_sum_fun_sum (fun k => (hX k).const_mul _) (fun k => (hX k).const_mul _)]
  simp_rw [covariance_const_mul_left, covariance_const_mul_right]
  simp only [Matrix.mul_apply, Matrix.of_apply, Matrix.transpose_apply, Finset.sum_mul]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro k _
  apply Finset.sum_congr rfl
  intro l _
  ring

private theorem isUnit_middle_of_congruence {n : Type*} [Fintype n] [DecidableEq n]
    (T G : Matrix n n ℝ) (h : IsUnit (T * G * T.transpose)) : IsUnit G := by
  rw [Matrix.isUnit_iff_isUnit_det, Matrix.det_mul, Matrix.det_mul,
    IsUnit.mul_iff, IsUnit.mul_iff] at h
  exact (Matrix.isUnit_iff_isUnit_det G).mpr h.1.2

/-- Equality of the actual raw/confluent covariance matrices, not a model covariance. -/
theorem rawPinCovariance_congruence {L : ℝ} (hL : L ≠ 0) (r : ℝ) (hr : r ≠ 0) :
    sourcePinCovarianceAt L r =
      confluentMatrix r hr * rawPinCovariance L r * (confluentMatrix r hr).transpose := by
  have : IsProbabilityMeasure (smoothLaw 2 L) := smoothLaw_isProbabilityMeasure 2 hL
  have h := covariance_matrix_congruence (smoothLaw 2 L) (rawPins L r)
    (fun i => ((rawPins_hasGaussianLaw hL r).eval i).memLp_two) (confluentMatrix r hr)
  simpa only [← sourceConfluentPinsAt_eq_matrix] using h

theorem rawPinCovariance_isUnit {L : ℝ} (hL : L ≠ 0) (r : ℝ) (hr : r ≠ 0)
    (hG : IsUnit (sourcePinCovarianceAt L r)) : IsUnit (rawPinCovariance L r) := by
  apply isUnit_middle_of_congruence (confluentMatrix r hr) (rawPinCovariance L r)
  rw [← rawPinCovariance_congruence hL r hr]
  exact hG

private theorem inverse_congruence {n : Type*} [Fintype n] [DecidableEq n]
    (T G : Matrix n n ℝ) (hT : IsUnit T) :
    T.transpose * (T * G * T.transpose)⁻¹ * T = G⁻¹ := by
  let _ : Invertible T := hT.invertible
  simp only [Matrix.mul_inv_rev, Matrix.mul_assoc,
    Matrix.inv_mul_of_invertible, Matrix.mul_one]
  rw [← Matrix.mul_assoc, Matrix.mul_inv_of_invertible, Matrix.one_mul]

private theorem inverse_congruence_mulVec {n : Type*} [Fintype n] [DecidableEq n]
    (T G : Matrix n n ℝ) (hT : IsUnit T) (y : n → ℝ) :
    T.transpose *ᵥ ((T * G * T.transpose)⁻¹ *ᵥ (T *ᵥ y)) = G⁻¹ *ᵥ y := by
  simpa only [Matrix.mulVec_mulVec, Matrix.mul_assoc] using
    congrArg (fun A : Matrix n n ℝ => A *ᵥ y) (inverse_congruence T G hT)

private theorem coefficient_lift_congr {n : Type*} [Fintype n] [DecidableEq n]
    (T G : Matrix n n ℝ) (hT : IsUnit T) (a y : n → ℝ) :
    (T *ᵥ a) ⬝ᵥ ((T * G * T.transpose)⁻¹ *ᵥ (T *ᵥ y)) = a ⬝ᵥ (G⁻¹ *ᵥ y) := by
  rw [dotProduct_comm, Matrix.dotProduct_mulVec, ← Matrix.mulVec_transpose,
    dotProduct_comm, inverse_congruence_mulVec T G hT]

/-- The literal raw covariance correction, retaining every target component. -/
def rawPinLift (L r : ℝ) (y : Fin 6 → ℝ) (m : SourceMode 2) : ℝ :=
  ∑ i, rawPinCoefficient L r i m * (((rawPinCovariance L r)⁻¹ *ᵥ y) i)

theorem rawPinLift_goodSample {L : ℝ} (hL : L ≠ 0) (r : ℝ) (y : Fin 6 → ℝ) :
    goodSample 2 L (rawPinLift L r y) := by
  intro n
  have hprod (i : Fin 6) : Summable (fun m =>
      orderModeBound n 2 L m * |rawPinCoefficient L r i m|) :=
    coefficient_product_summable (orderModeBound_summable n 2 hL)
      (rawPinCoefficient_summable hL r i).abs
  have hs : Summable (fun m => ∑ i,
      (orderModeBound n 2 L m * |rawPinCoefficient L r i m|) *
        |((rawPinCovariance L r)⁻¹ *ᵥ y) i|) :=
    summable_sum (fun i _ => (hprod i).mul_right _)
  apply Summable.of_nonneg_of_le (fun m =>
    mul_nonneg (orderModeBound_nonneg n 2 L m) (abs_nonneg _)) _ hs
  intro m
  calc
    _ ≤ orderModeBound n 2 L m *
        ∑ i, |rawPinCoefficient L r i m * (((rawPinCovariance L r)⁻¹ *ᵥ y) i)| :=
      mul_le_mul_of_nonneg_left (Finset.abs_sum_le_sum_abs _ _) (orderModeBound_nonneg n 2 L m)
    _ = _ := by simp only [abs_mul, Finset.mul_sum, mul_assoc]

theorem rawPinLift_measurable (L r : ℝ) : Measurable (rawPinLift L r) := by
  apply Measurable.of_eval
  intro m
  unfold rawPinLift
  fun_prop

/-- The same coefficient lift at every target. This sampling identity also holds
under the nonsingular-inverse convention before current covariance invertibility. -/
theorem pinLift_confluent_eq_raw {L : ℝ} (hL : L ≠ 0) (r : ℝ) (hr : r ≠ 0)
    (y : Fin 6 → ℝ) (m : SourceMode 2) :
    pinLift L r (confluentTransform r y) m = rawPinLift L r y m := by
  change (fun i => pinCoefficient L r i m) ⬝ᵥ
      ((sourcePinCovarianceAt L r)⁻¹ *ᵥ confluentTransform r y) =
    (fun i => rawPinCoefficient L r i m) ⬝ᵥ ((rawPinCovariance L r)⁻¹ *ᵥ y)
  rw [← confluentMatrix_mulVec r hr y, pinCoefficient_eq_confluentMatrix,
    rawPinCovariance_congruence hL r hr]
  exact coefficient_lift_congr _ _ (confluentMatrix_isUnit r hr) _ y

/-- This map is the actual raw coefficient regression, not a chosen value on a raw fiber. -/
def rawPosteriorSample {L : ℝ} (hL : L ≠ 0) (r : ℝ) (t : Fin 6 → ℝ)
    (ω : SmoothSample 2 L) : SmoothSample 2 L :=
  ⟨sampleInclusion 2 L ω + rawPinLift L r (t - rawPins L r ω),
    goodSample_add _ _ ω.property (rawPinLift_goodSample hL r _)⟩

theorem rawPosteriorSample_val {L : ℝ} (hL : L ≠ 0) (r : ℝ) (t : Fin 6 → ℝ)
    (ω : SmoothSample 2 L) (m : SourceMode 2) :
    (rawPosteriorSample hL r t ω).val m =
      ω.val m + rawPinLift L r (t - rawPins L r ω) m := rfl

theorem rawPosteriorSample_measurable {L : ℝ} (hL : L ≠ 0) (r : ℝ) :
    Measurable (fun p : (Fin 6 → ℝ) × SmoothSample 2 L => rawPosteriorSample hL r p.1 p.2) := by
  unfold rawPosteriorSample
  apply Measurable.subtype_mk
  exact ((sampleInclusion_measurable 2 L).comp measurable_snd).add
    ((rawPinLift_measurable L r).comp
      (measurable_fst.sub ((rawPins_measurable hL r).comp measurable_snd)))

/-- Pointwise equality on the entire original carrier, not only on a zero-pin fiber. -/
theorem rawPosteriorSample_eq_posteriorSample {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (hr : r ≠ 0) (t : Fin 6 → ℝ) (ω : SmoothSample 2 L) :
    rawPosteriorSample hL r t ω = posteriorSample hL r (confluentTransform r t) ω := by
  apply Subtype.ext
  funext m
  rw [rawPosteriorSample_val, posteriorSample_val]
  have hy : confluentTransform r t - sourceConfluentPinsAt L r ω =
      confluentTransform r (t - rawPins L r ω) := by
    change confluentEquiv r hr t - confluentEquiv r hr (rawPins L r ω) =
      confluentEquiv r hr (t - rawPins L r ω)
    exact (map_sub (confluentEquiv r hr) t (rawPins L r ω)).symm
  rw [hy, pinLift_confluent_eq_raw hL r hr]

/-- Literal raw posterior sampling kernel, specified at every target. -/
def rawPinKernel {L : ℝ} (hL : L ≠ 0) (r : ℝ) :
    Kernel (Fin 6 → ℝ) (SmoothSample 2 L) :=
  ((Kernel.id : Kernel (Fin 6 → ℝ) (Fin 6 → ℝ)) ×ₖ
    Kernel.const (Fin 6 → ℝ) (smoothLaw 2 L)).map
      (fun p => rawPosteriorSample hL r p.1 p.2)

instance rawPinKernel_isMarkov {L : ℝ} (hL : L ≠ 0) (r : ℝ) :
    IsMarkovKernel (rawPinKernel hL r) := by
  have : IsProbabilityMeasure (smoothLaw 2 L) := smoothLaw_isProbabilityMeasure 2 hL
  exact Kernel.IsMarkovKernel.map _ (rawPosteriorSample_measurable hL r)

theorem rawPinKernel_apply {L : ℝ} (hL : L ≠ 0) (r : ℝ) (t : Fin 6 → ℝ) :
    rawPinKernel hL r t = (smoothLaw 2 L).map (rawPosteriorSample hL r t) := by
  have : IsProbabilityMeasure (smoothLaw 2 L) := smoothLaw_isProbabilityMeasure 2 hL
  rw [rawPinKernel, Kernel.map_apply _ (rawPosteriorSample_measurable hL r),
    Kernel.prod_apply, Kernel.id_apply, Kernel.const_apply, Measure.dirac_prod]
  rfl

/-- Every target, including any prescribed probability-zero pin, uses the same sample map. -/
theorem rawPinKernel_eq_confluent {L : ℝ} (hL : L ≠ 0) (r : ℝ) (hr : r ≠ 0)
    (t : Fin 6 → ℝ) :
    rawPinKernel hL r t = sourceSmoothKernel hL r (confluentTransform r t) := by
  rw [rawPinKernel_apply, sourceSmoothKernel_apply]
  congr 1
  funext ω
  exact rawPosteriorSample_eq_posteriorSample hL r hr t ω

theorem rawPinKernel_eq_comap {L : ℝ} (hL : L ≠ 0) (r : ℝ) (hr : r ≠ 0) :
    rawPinKernel hL r = (sourceSmoothKernel hL r).comap (confluentEquiv r hr)
      (confluentEquiv r hr).continuous.measurable := by
  ext t : 1
  exact rawPinKernel_eq_confluent hL r hr t

/-- Transport the already proved whole-carrier RCD through the inverse measurable
observation equivalence. Residual independence is reused, not assumed or reproved. -/
theorem rawPinKernel_hasCondDistrib {L : ℝ} (hL : L ≠ 0) (r : ℝ) (hr : r ≠ 0)
    (hG : IsUnit (sourcePinCovarianceAt L r)) :
    HasCondDistrib (id : SmoothSample 2 L → SmoothSample 2 L)
      (rawPins L r) (rawPinKernel hL r) (smoothLaw 2 L) := by
  let e : (Fin 6 → ℝ) ≃ᵐ (Fin 6 → ℝ) :=
    (confluentEquiv r hr).toHomeomorph.toMeasurableEquiv
  have hc := (sourceSmoothKernel_hasCondDistrib hL r hG).measurableEquiv_comp_right e.symm
  have hobs : e.symm ∘ sourceConfluentPinsAt L r = rawPins L r := by
    funext ω
    exact rawTransform_confluentTransform r hr (rawPins L r ω)
  have hkernel : (sourceSmoothKernel hL r).comap e e.measurable = rawPinKernel hL r := by
    ext t : 1
    exact (rawPinKernel_eq_confluent hL r hr t).symm
  simpa only [MeasurableEquiv.symm_symm, hobs, hkernel] using hc

theorem rawPinKernel_map_hasCondDistrib {L : ℝ} (hL : L ≠ 0) (r : ℝ) (hr : r ≠ 0)
    (hG : IsUnit (sourcePinCovarianceAt L r)) {E : Type*} [MeasurableSpace E]
    (F : SmoothSample 2 L → E) (hF : Measurable F) :
    HasCondDistrib F (rawPins L r) ((rawPinKernel hL r).map F) (smoothLaw 2 L) := by
  have : IsProbabilityMeasure (smoothLaw 2 L) := smoothLaw_isProbabilityMeasure 2 hL
  simpa only [Function.comp_id] using
    (rawPinKernel_hasCondDistrib hL r hr hG).comp_left hF

theorem rawPinCovariance_eventually_isUnit {L : ℝ} (hL : L ≠ 0) :
    ∀ᶠ r in 𝓝[>] (0 : ℝ), IsUnit (rawPinCovariance L r) := by
  filter_upwards [(sourceEndpoint_parameter_limits hL 0).1, self_mem_nhdsWithin] with r hG hr
  exact rawPinCovariance_isUnit hL r (ne_of_gt hr) hG

theorem rawPinKernel_eventually_hasCondDistrib {L : ℝ} (hL : L ≠ 0) :
    ∀ᶠ r in 𝓝[>] (0 : ℝ),
      HasCondDistrib (id : SmoothSample 2 L → SmoothSample 2 L)
        (rawPins L r) (rawPinKernel hL r) (smoothLaw 2 L) := by
  filter_upwards [(sourceEndpoint_parameter_limits hL 0).1, self_mem_nhdsWithin] with r hG hr
  exact rawPinKernel_hasCondDistrib hL r (ne_of_gt hr) hG

/-- The literal raw target keeps the arbitrary height and the cubic gap. -/
theorem rawPinKernel_prescribed {L : ℝ} (hL : L ≠ 0) (r b : ℝ) (hr : r ≠ 0) :
    rawPinKernel hL r ![b, b-r^3/6, 0, 0, 0, 0] = sourceSmoothLaw hL r b := by
  rw [rawPinKernel_eq_confluent hL r hr]
  change sourceSmoothKernel hL r (confluentEquiv r hr ![b,b-r^3/6,0,0,0,0]) = _
  rw [prescribed_target]
  rfl

/-- A measure at every parameter; probability follows from the proved positive floor. -/
def rawPrescribedWeightedMeasure {L : ℝ} (hL : L ≠ 0) (r b : ℝ) :
    Measure (SmoothSample 2 L) :=
  prwMeasure (rawPinKernel hL r ![b,b-r^3/6,0,0,0,0]) (sourceSmoothWeight L r)

theorem rawPrescribedWeightedMeasure_eq {L : ℝ} (hL : L ≠ 0) (r b : ℝ) (hr : r ≠ 0) :
    rawPrescribedWeightedMeasure hL r b = sourceSmoothWeightedLaw hL r b := by
  unfold rawPrescribedWeightedMeasure sourceSmoothWeightedLaw
  rw [rawPinKernel_prescribed hL r b hr]

/-- All moment, normalizer, probability, event and support facts are the existing
actual source estimates rewritten through the every-target raw kernel identity. -/
theorem rawPrescribedWeightedMeasure_estimates {L : ℝ} (hL : L ≠ 0) (b : ℝ) :
    ∃ C c δ : ℝ, 0 ≤ C ∧ 0 < c ∧ 0 < δ ∧ δ ≤ 1 ∧
      ∀ r : ℝ, 0 < r → r < δ →
        Integrable (fun ω => sourceSmoothWeight L r ω ^ 2)
          (rawPinKernel hL r ![b,b-r^3/6,0,0,0,0]) ∧
        (∫ ω, sourceSmoothWeight L r ω ^ 2
          ∂rawPinKernel hL r ![b,b-r^3/6,0,0,0,0]) ≤ C*r^4 ∧
        c*r^2 ≤ (∫ ω, sourceSmoothWeight L r ω
          ∂rawPinKernel hL r ![b,b-r^3/6,0,0,0,0]) ∧
        IsProbabilityMeasure (rawPrescribedWeightedMeasure hL r b) ∧
        (∀ E : Set (SmoothSample 2 L), MeasurableSet E →
          (rawPrescribedWeightedMeasure hL r b).real E ≤ (Real.sqrt C/c) *
            Real.sqrt ((rawPinKernel hL r ![b,b-r^3/6,0,0,0,0]).real E)) ∧
        (rawPrescribedWeightedMeasure hL r b).map (sourceNormalizedEndpoints L r) =
          sourcePhysicalEndpointWeightedProbability L r b ∧
        rawPrescribedWeightedMeasure hL r b
          {ω | rawPins L r ω = ![b,b-r^3/6,0,0,0,0]} = 1 ∧
        rawPrescribedWeightedMeasure hL r b {ω | sourceSmoothTyped L r ω} = 1 := by
  obtain ⟨C,c,δ,hC,hc,hδ,hδ1,hest⟩ := sourceSmoothPalm_estimates hL b
  refine ⟨C,c,δ,hC,hc,hδ,hδ1,?_⟩
  intro r hr hrδ
  simpa only [rawPinKernel_prescribed hL r b hr.ne',
    rawPrescribedWeightedMeasure_eq hL r b hr.ne'] using hest r hr hrδ

end I4SourceRawPinConditioning
