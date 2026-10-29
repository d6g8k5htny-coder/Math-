import SourceConditionalMajorant

/-!+# Actual scalar curvature direction and full-carrier reconstruction

Every Gaussian law and independence assertion below comes from the literal
Fourier coefficients on the existing smooth sample carrier. See
SOURCE_CURVATURE_DECOMPOSITION.md. Author-side formal work is separate from
scientific review and geometric Palm identification.
-/

noncomputable section

open I4Foundation I4Source I4Smooth I4SmoothCarrier I4SourceGaussian I4SourceCovariance
open I4SourceDerivativeGaussian I4SourceDerivativeContinuity I4SourceConfluentPins
open I4SourceConfluentLimits I4ContactCoefficientLimits I4SourceEndpointRegression
open I4SourceContact I4SourceSmoothConditional I4SourceConditionalMajorant I4ContactGram
open I4GaussianRegressionLimits I4SourceEndpointEstimates MeasureTheory ProbabilityTheory Matrix Filter
open scoped BigOperators Topology NNReal

set_option autoImplicit false

namespace I4SourceCurvatureDecomposition

def curvatureCoefficient (L : ℝ) (m : SourceMode 2) : ℝ :=
  sourceContactCoefficient L 6 m

def curvatureCross (L r : ℝ) (i : Fin 6) : ℝ :=
  covariance (sourceContactQ L) (fun ω => sourceConfluentPinsAt L r ω i) (smoothLaw 2 L)

def curvatureBeta (L r : ℝ) : Fin 6 → ℝ :=
  curvatureCross L r ᵥ* (sourcePinCovarianceAt L r)⁻¹

def curvatureMean (L r : ℝ) (x : Fin 6 → ℝ) : ℝ := curvatureBeta L r ⬝ᵥ x

def curvatureVariance (L r : ℝ) : ℝ :=
  Var[sourceContactQ L; smoothLaw 2 L] - curvatureBeta L r ⬝ᵥ curvatureCross L r

def curvatureSigma (L r : ℝ) : ℝ := Real.sqrt (curvatureVariance L r)

def curvatureResidualCoefficient (L r : ℝ) (m : SourceMode 2) : ℝ :=
  curvatureCoefficient L m - ∑ i, curvatureBeta L r i * pinCoefficient L r i m

def curvatureDirection (L r : ℝ) (m : SourceMode 2) : ℝ :=
  curvatureResidualCoefficient L r m / curvatureSigma L r

def curvatureZ (L r : ℝ) (ω : SmoothSample 2 L) : ℝ :=
  scalarSeries (curvatureDirection L r) ω.val

theorem curvatureCoefficient_summable {L : ℝ} (hL : L ≠ 0) :
    Summable (curvatureCoefficient L) := sourceContactCoefficient_summable hL 6

theorem sourceContactQ_series {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    sourceContactQ L ω = scalarSeries (curvatureCoefficient L) ω.val :=
  smoothSourceField_derivative_series 2 hL ω 2 0 ![contactE1,contactE1]

theorem curvatureCoefficient_weighted_summable {L : ℝ} (hL : L ≠ 0)
    (ω : SmoothSample 2 L) :
    Summable (fun m => curvatureCoefficient L m * ω.val m) :=
  derivativeCoefficient_weighted_summable hL ω 2 0 ![contactE1,contactE1]

theorem curvatureCross_coefficient {L : ℝ} (hL : L ≠ 0) (r : ℝ) (i : Fin 6) :
    curvatureCross L r i = ∑' m, curvatureCoefficient L m * pinCoefficient L r i m := by
  unfold curvatureCross
  have hQ : sourceContactQ L = fun ω => scalarSeries (curvatureCoefficient L) ω.val :=
    funext (sourceContactQ_series hL)
  have hX : (fun ω => sourceConfluentPinsAt L r ω i) =
      fun ω => scalarSeries (pinCoefficient L r i) ω.val := by
    funext ω
    exact congrFun (sourceConfluentPinsAt_series hL r ω) i
  rw [hQ,hX]
  change covariance (fun ω => scalarSeries (curvatureCoefficient L) (sampleInclusion 2 L ω))
    (fun ω => scalarSeries (pinCoefficient L r i) (sampleInclusion 2 L ω)) (smoothLaw 2 L) = _
  rw [covariance_comp_inclusion 2 hL _ _ (scalarSeries_measurable _) (scalarSeries_measurable _)]
  exact scalarSeries_covariance _ _ (curvatureCoefficient_summable hL) (pinCoefficient_summable hL r i)

theorem curvatureVariance_prior_coefficient {L : ℝ} (hL : L ≠ 0) :
    Var[sourceContactQ L; smoothLaw 2 L] = ∑' m, curvatureCoefficient L m * curvatureCoefficient L m := by
  change Var[fun ω => sourceContactVector L ω 6; smoothLaw 2 L] = _
  rw [← sourceContactQVariance_eq_variance hL]
  change sourceContactCovariance L 6 6 = _
  rw [sourceContactCovariance_eq_coefficientGram hL]
  rfl

theorem curvatureResidualCoefficient_summable {L : ℝ} (hL : L ≠ 0) (r : ℝ) :
    Summable (curvatureResidualCoefficient L r) :=
  (curvatureCoefficient_summable hL).sub
    (summable_sum (fun i _ => (pinCoefficient_summable hL r i).mul_left _))

theorem curvatureDirection_summable {L : ℝ} (hL : L ≠ 0) (r : ℝ) :
    Summable (curvatureDirection L r) :=
  (curvatureResidualCoefficient_summable hL r).div_const _

theorem curvatureBeta_normal (L r : ℝ) (hG : IsUnit (sourcePinCovarianceAt L r)) :
    curvatureBeta L r ᵥ* sourcePinCovarianceAt L r = curvatureCross L r := by
  let _ : Invertible (sourcePinCovarianceAt L r) := hG.invertible
  rw [curvatureBeta, Matrix.vecMul_vecMul, Matrix.inv_mul_of_invertible, Matrix.vecMul_one]

end I4SourceCurvatureDecomposition

namespace I4SourceCurvatureDecomposition

private lemma pairing_sub_finite {ι : Type*} {n : ℕ}
    (a b : ι → ℝ) (c : Fin n → ι → ℝ) (z : Fin n → ℝ)
    (ha : Summable a) (hb : Summable b) (hc : ∀ i, Summable (c i)) :
    (∑' m, a m * (b m - ∑ i, z i * c i m)) =
      (∑' m, a m * b m) - ∑ i, z i * (∑' m, a m * c i m) := by
  have hs : HasSum (fun m => ∑ i, z i * (a m * c i m))
      (∑ i, z i * (∑' m, a m * c i m)) :=
    hasSum_sum (fun i _ => ((coefficient_product_summable ha (hc i)).hasSum).mul_left (z i))
  have ht := (coefficient_product_summable ha hb).hasSum.sub hs
  convert ht.tsum_eq using 1
  apply tsum_congr
  intro m
  rw [mul_sub, Finset.mul_sum]
  congr 1
  apply Finset.sum_congr rfl
  intro i _
  ring

theorem curvatureResidual_pin_orthogonal {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (hG : IsUnit (sourcePinCovarianceAt L r)) (i : Fin 6) :
    (∑' m, pinCoefficient L r i m * curvatureResidualCoefficient L r m) = 0 := by
  change (∑' m, pinCoefficient L r i m *
    (curvatureCoefficient L m - ∑ j, curvatureBeta L r j * pinCoefficient L r j m)) = 0
  rw [pairing_sub_finite _ _ _ _ (pinCoefficient_summable hL r i)
    (curvatureCoefficient_summable hL) (pinCoefficient_summable hL r)]
  have hfirst : (∑' m, pinCoefficient L r i m * curvatureCoefficient L m) =
      curvatureCross L r i := by
    rw [curvatureCross_coefficient hL r i]
    apply tsum_congr
    intro m
    ring
  rw [hfirst]
  simp_rw [← sourcePinCovarianceAt_coefficient hL r]
  have hn : (∑ j, curvatureBeta L r j * sourcePinCovarianceAt L r i j) =
      curvatureCross L r i := by
    calc
      _ = (curvatureBeta L r ᵥ* sourcePinCovarianceAt L r) i := by
        change (∑ j, curvatureBeta L r j * sourcePinCovarianceAt L r i j) =
          ∑ j, curvatureBeta L r j * sourcePinCovarianceAt L r j i
        apply Finset.sum_congr rfl
        intro j _
        congr 1
        exact covariance_comm _ _
      _ = _ := congrFun (curvatureBeta_normal L r hG) i
  rw [hn, sub_self]

theorem curvatureResidual_q_pairing {L : ℝ} (hL : L ≠ 0) (r : ℝ) :
    (∑' m, curvatureCoefficient L m * curvatureResidualCoefficient L r m) =
      curvatureVariance L r := by
  change (∑' m, curvatureCoefficient L m *
    (curvatureCoefficient L m - ∑ j, curvatureBeta L r j * pinCoefficient L r j m)) = _
  rw [pairing_sub_finite _ _ _ _ (curvatureCoefficient_summable hL)
    (curvatureCoefficient_summable hL) (pinCoefficient_summable hL r),
    ← curvatureVariance_prior_coefficient hL]
  simp_rw [← curvatureCross_coefficient hL r]
  rfl

theorem curvatureResidual_normSquared {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (hG : IsUnit (sourcePinCovarianceAt L r)) :
    (∑' m, curvatureResidualCoefficient L r m ^ 2) = curvatureVariance L r := by
  have hs := pairing_sub_finite (curvatureResidualCoefficient L r)
    (curvatureCoefficient L) (pinCoefficient L r) (curvatureBeta L r)
    (curvatureResidualCoefficient_summable hL r) (curvatureCoefficient_summable hL)
    (pinCoefficient_summable hL r)
  have hp (i : Fin 6) : (∑' m, curvatureResidualCoefficient L r m * pinCoefficient L r i m) = 0 := by
    calc
      _ = ∑' m, pinCoefficient L r i m * curvatureResidualCoefficient L r m := by
        apply tsum_congr
        intro m
        ring
      _ = 0 := curvatureResidual_pin_orthogonal hL r hG i
  simp only [pow_two]
  change (∑' m, curvatureResidualCoefficient L r m * curvatureResidualCoefficient L r m) = _ at hs
  rw [hs]
  simp_rw [hp, mul_zero, Finset.sum_const_zero, sub_zero]
  calc
    _ = ∑' m, curvatureCoefficient L m * curvatureResidualCoefficient L r m := by
      apply tsum_congr
      intro m
      ring
    _ = _ := curvatureResidual_q_pairing hL r

theorem curvatureDirection_pin_orthogonal {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (hG : IsUnit (sourcePinCovarianceAt L r)) (i : Fin 6) :
    (∑' m, pinCoefficient L r i m * curvatureDirection L r m) = 0 := by
  simp only [curvatureDirection, ← mul_div_assoc, tsum_div_const,
    curvatureResidual_pin_orthogonal hL r hG, zero_div]

theorem curvatureSigma_pos {L r : ℝ} (hτ : 0 < curvatureVariance L r) :
    0 < curvatureSigma L r := Real.sqrt_pos.mpr hτ

theorem curvatureSigma_sq {L r : ℝ} (hτ : 0 < curvatureVariance L r) :
    curvatureSigma L r ^ 2 = curvatureVariance L r := Real.sq_sqrt hτ.le

theorem curvatureDirection_normSquared {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (hG : IsUnit (sourcePinCovarianceAt L r)) (hτ : 0 < curvatureVariance L r) :
    (∑' m, curvatureDirection L r m ^ 2) = 1 := by
  simp only [curvatureDirection, div_pow, tsum_div_const,
    curvatureResidual_normSquared hL r hG, curvatureSigma_sq hτ, div_self hτ.ne']

theorem curvatureDirection_q_pairing {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (hτ : 0 < curvatureVariance L r) :
    (∑' m, curvatureCoefficient L m * curvatureDirection L r m) = curvatureSigma L r := by
  simp only [curvatureDirection, ← mul_div_assoc, tsum_div_const, curvatureResidual_q_pairing hL r]
  apply (div_eq_iff (curvatureSigma_pos hτ).ne').2
  simpa only [pow_two] using (curvatureSigma_sq hτ).symm

theorem curvatureResidualCoefficient_weighted_summable {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (ω : SmoothSample 2 L) :
    Summable (fun m => curvatureResidualCoefficient L r m * ω.val m) := by
  have hsum : Summable (fun m => ∑ i : Fin 6,
      curvatureBeta L r i * (pinCoefficient L r i m * ω.val m)) :=
    summable_sum (fun i _ => (pinCoefficient_weighted_summable hL r ω i).mul_left (curvatureBeta L r i))
  have h := (curvatureCoefficient_weighted_summable hL ω).sub hsum
  convert h using 1
  funext m
  simp only [curvatureResidualCoefficient, sub_mul, Finset.sum_mul, mul_assoc]

theorem curvatureDirection_weighted_summable {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (ω : SmoothSample 2 L) :
    Summable (fun m => curvatureDirection L r m * ω.val m) := by
  have h := (curvatureResidualCoefficient_weighted_summable hL r ω).div_const (curvatureSigma L r)
  convert h using 1
  funext m
  simp only [curvatureDirection, div_mul_eq_mul_div]

private lemma scalarSeries_sub_finite {ι : Type*} {n : ℕ}
    (a : ι → ℝ) (b : Fin n → ι → ℝ) (ω : ι → ℝ) (z : Fin n → ℝ)
    (ha : Summable (fun m => a m * ω m))
    (hb : ∀ i, Summable (fun m => b i m * ω m)) :
    scalarSeries (fun m => a m - ∑ i, z i * b i m) ω =
      scalarSeries a ω - ∑ i, z i * scalarSeries (b i) ω := by
  have hs : HasSum (fun m => ∑ i, z i * (b i m * ω m))
      (∑ i, z i * scalarSeries (b i) ω) :=
    hasSum_sum (fun i _ => ((hb i).hasSum).mul_left (z i))
  have ht := ha.hasSum.sub hs
  change (∑' m, (a m - ∑ i, z i * b i m) * ω m) = _
  convert ht.tsum_eq using 1
  · apply tsum_congr
    intro m
    simp only [sub_mul, Finset.sum_mul, mul_assoc]
  · rfl

theorem curvatureZ_eq {L : ℝ} (hL : L ≠ 0) (r : ℝ) (ω : SmoothSample 2 L) :
    curvatureZ L r ω = (sourceContactQ L ω - curvatureMean L r (sourceConfluentPinsAt L r ω)) /
      curvatureSigma L r := by
  unfold curvatureZ curvatureDirection
  have hd : scalarSeries (curvatureResidualCoefficient L r) ω.val =
      sourceContactQ L ω - curvatureMean L r (sourceConfluentPinsAt L r ω) := by
    change scalarSeries (fun m => curvatureCoefficient L m -
      ∑ i, curvatureBeta L r i * pinCoefficient L r i m) ω.val = _
    rw [scalarSeries_sub_finite _ _ _ _
      (curvatureCoefficient_weighted_summable hL ω)
      (pinCoefficient_weighted_summable hL r ω), ← sourceContactQ_series hL ω]
    congr 1
    change (∑ i, curvatureBeta L r i * scalarSeries (pinCoefficient L r i) ω.val) =
      ∑ i, curvatureBeta L r i * sourceConfluentPinsAt L r ω i
    apply Finset.sum_congr rfl
    intro i _
    rw [congrFun (sourceConfluentPinsAt_series hL r ω) i]
    rfl
  simpa only [scalarSeries, div_mul_eq_mul_div, tsum_div_const] using congrArg
    (fun t : ℝ => t / curvatureSigma L r) hd

end I4SourceCurvatureDecomposition

/- Coauthored by /root/normalizer_palm_research/gaussian_reference_probe;
compiled scratch Direction.lean; no scientific-review credit. -/
namespace I4SourceCurvatureDecomposition

def unitDirection {L : ℝ} (χ : SourceMode 2 → ℝ) (ω : SmoothSample 2 L) : ℝ :=
  scalarSeries χ ω.val

def unitDirectionCoefficientResidual {L : ℝ} (χ : SourceMode 2 → ℝ)
    (ω : SmoothSample 2 L) (m : SourceMode 2) : ℝ :=
  ω.val m - χ m * unitDirection χ ω

theorem unitDirection_measurable {L : ℝ} (χ : SourceMode 2 → ℝ) :
    Measurable (unitDirection (L := L) χ) :=
  (scalarSeries_measurable χ).comp measurable_subtype_coe

theorem unitDirection_hasLaw {L : ℝ} (hL : L ≠ 0) (χ : SourceMode 2 → ℝ)
    (hχ : Summable χ) (hnorm : (∑' m, χ m ^ 2) = 1) :
    HasLaw (unitDirection (L := L) χ) (gaussianReal 0 1) (smoothLaw 2 L) where
  aemeasurable := (unitDirection_measurable χ).aemeasurable
  map_eq := by
    change (smoothLaw 2 L).map (fun ω => scalarSeries χ (sampleInclusion 2 L ω)) = _
    rw [observation_map_eq 2 hL _ (scalarSeries_measurable χ), scalarSeries_map_gaussian χ hχ, hnorm]
    norm_num

theorem unitDirection_coefficient_covariance {L : ℝ} (hL : L ≠ 0)
    (χ : SourceMode 2 → ℝ) (hχ : Summable χ) (m : SourceMode 2) :
    covariance (unitDirection (L := L) χ) (fun ω : SmoothSample 2 L => ω.val m)
      (smoothLaw 2 L) = χ m := by
  change covariance (fun ω => scalarSeries χ (sampleInclusion 2 L ω))
    (fun ω => sampleInclusion 2 L ω m) (smoothLaw 2 L) = _
  rw [covariance_comp_inclusion 2 hL _ _ (scalarSeries_measurable χ) (measurable_pi_apply m)]
  exact scalarSeries_coordinate_covariance χ hχ m

theorem unitDirectionCoefficientResidual_zero_covariance {L : ℝ} (hL : L ≠ 0)
    (χ : SourceMode 2 → ℝ) (hχ : Summable χ) (hnorm : (∑' m, χ m ^ 2) = 1)
    (m : SourceMode 2) :
    covariance (unitDirection (L := L) χ) (fun ω => unitDirectionCoefficientResidual χ ω m)
      (smoothLaw 2 L) = 0 := by
  have hZ := unitDirection_hasLaw hL χ hχ hnorm
  have hZG := hZ.hasGaussianLaw
  have : IsProbabilityMeasure (smoothLaw 2 L) := smoothLaw_isProbabilityMeasure 2 hL
  have hvar : Var[unitDirection (L := L) χ; smoothLaw 2 L] = 1 := by
    rw [hZ.variance_eq, variance_id_gaussianReal]
    norm_num
  unfold unitDirectionCoefficientResidual
  rw [covariance_fun_sub_right hZG.memLp_two (coefficient_hasGaussianLaw hL m).memLp_two
    (hZG.memLp_two.const_mul (χ m)), covariance_const_mul_right,
    unitDirection_coefficient_covariance hL χ hχ m, covariance_self hZG.aemeasurable, hvar]
  ring

theorem unitDirection_finiteCoefficients_hasGaussianLaw {L : ℝ} (hL : L ≠ 0)
    (χ : SourceMode 2 → ℝ) (hχ : Summable χ) (I : Finset (SourceMode 2)) :
    HasGaussianLaw (fun ω : SmoothSample 2 L =>
      ((fun _ : Fin 1 => unitDirection χ ω), fun m : I => ω.val m)) (smoothLaw 2 L) := by
  classical
  let q : (Fin 1 ⊕ I) → SourceMode 2 → ℝ :=
    Sum.elim (fun _ => χ) (fun m => Pi.single m.val 1)
  have hq (j : Fin 1 ⊕ I) : Summable (q j) := by
    cases j with
    | inl i => exact hχ
    | inr m =>
      apply summable_of_ne_finset_zero (s := {m.val})
      intro n hn
      simp only [Finset.mem_singleton] at hn
      simp [q, hn]
  have hG := scalarSeries_finite_hasGaussianLaw q hq
  have hm : Measurable (fun η j => scalarSeries (q j) η) :=
    Measurable.of_eval (fun j => scalarSeries_measurable (q j))
  have hμ : HasGaussianLaw (fun ω : SmoothSample 2 L =>
      fun j => scalarSeries (q j) (sampleInclusion 2 L ω)) (smoothLaw 2 L) := by
    refine ⟨(hm.comp (sampleInclusion_measurable 2 L)).aemeasurable, ?_⟩
    rw [observation_map_eq 2 hL _ hm]
    exact hG.isGaussian_map
  let A : ((Fin 1 ⊕ I) → ℝ) →L[ℝ] ((Fin 1 → ℝ) × (I → ℝ)) :=
    (ContinuousLinearMap.pi (fun i => ContinuousLinearMap.proj (Sum.inl i))).prod
      (ContinuousLinearMap.pi (fun m => ContinuousLinearMap.proj (Sum.inr m)))
  apply (hμ.map_fun A).congr
  filter_upwards with ω
  apply Prod.ext
  · rfl
  · funext m
    exact scalarSeries_single m.val ω.val

def finiteDirectionLift (χ : SourceMode 2 → ℝ) (I : Finset (SourceMode 2)) :
    (Fin 1 → ℝ) →L[ℝ] (I → ℝ) :=
  ContinuousLinearMap.pi (fun m => χ m.val • ContinuousLinearMap.proj 0)

lemma finiteDirectionLift_apply (χ : SourceMode 2 → ℝ) (I : Finset (SourceMode 2))
    (z : Fin 1 → ℝ) (m : I) : finiteDirectionLift χ I z m = χ m.val * z 0 := rfl

theorem unitDirection_finiteResidual_hasGaussianLaw {L : ℝ} (hL : L ≠ 0)
    (χ : SourceMode 2 → ℝ) (hχ : Summable χ) (I : Finset (SourceMode 2)) :
    HasGaussianLaw (fun ω : SmoothSample 2 L =>
      ((fun _ : Fin 1 => unitDirection χ ω), fun m : I => unitDirectionCoefficientResidual χ ω m.val))
      (smoothLaw 2 L) := by
  let A : ((Fin 1 → ℝ) × (I → ℝ)) →L[ℝ] ((Fin 1 → ℝ) × (I → ℝ)) :=
    (ContinuousLinearMap.fst ℝ (Fin 1 → ℝ) (I → ℝ)).prod
      (ContinuousLinearMap.snd ℝ (Fin 1 → ℝ) (I → ℝ) -
        (finiteDirectionLift χ I).comp (ContinuousLinearMap.fst ℝ (Fin 1 → ℝ) (I → ℝ)))
  apply ((unitDirection_finiteCoefficients_hasGaussianLaw hL χ hχ I).map_fun A).congr
  filter_upwards with ω
  apply Prod.ext
  · rfl
  · rfl

theorem unitDirection_scalar_finiteResidual_hasGaussianLaw {L : ℝ} (hL : L ≠ 0)
    (χ : SourceMode 2 → ℝ) (hχ : Summable χ) (I : Finset (SourceMode 2)) :
    HasGaussianLaw (fun ω : SmoothSample 2 L =>
      (unitDirection χ ω, fun m : I => unitDirectionCoefficientResidual χ ω m.val))
      (smoothLaw 2 L) := by
  let A : ((Fin 1 → ℝ) × (I → ℝ)) →L[ℝ] (ℝ × (I → ℝ)) :=
    ((ContinuousLinearMap.proj 0).comp (ContinuousLinearMap.fst ℝ (Fin 1 → ℝ) (I → ℝ))).prod
      (ContinuousLinearMap.snd ℝ (Fin 1 → ℝ) (I → ℝ))
  apply ((unitDirection_finiteResidual_hasGaussianLaw hL χ hχ I).map_fun A).congr
  filter_upwards with ω
  rfl

theorem unitDirectionCoefficientResidual_finite_indepFun {L : ℝ} (hL : L ≠ 0)
    (χ : SourceMode 2 → ℝ) (hχ : Summable χ) (hnorm : (∑' m, χ m ^ 2) = 1)
    (I : Finset (SourceMode 2)) :
    IndepFun (unitDirection (L := L) χ)
      (fun (ω : SmoothSample 2 L) (m : I) => unitDirectionCoefficientResidual χ ω m.val) (smoothLaw 2 L) := by
  have h := (unitDirection_finiteResidual_hasGaussianLaw hL χ hχ I).indepFun_of_covariance_eval
    (fun _ m => unitDirectionCoefficientResidual_zero_covariance hL χ hχ hnorm m.val)
  exact h.comp (show Measurable (fun z : Fin 1 → ℝ => z 0) by fun_prop) measurable_id

theorem unitDirectionCoefficientResidual_indepFun {L : ℝ} (hL : L ≠ 0)
    (χ : SourceMode 2 → ℝ) (hχ : Summable χ) (hnorm : (∑' m, χ m ^ 2) = 1) :
    IndepFun (unitDirection (L := L) χ) (fun ω m => unitDirectionCoefficientResidual χ ω m)
      (smoothLaw 2 L) := by
  have : IsProbabilityMeasure (smoothLaw 2 L) := smoothLaw_isProbabilityMeasure 2 hL
  apply IndepFun.indepFun_process (unitDirection_measurable χ)
  · intro m
    exact ((measurable_pi_apply m).comp measurable_subtype_coe).sub
      (measurable_const.mul (unitDirection_measurable χ))
  · exact unitDirectionCoefficientResidual_finite_indepFun hL χ hχ hnorm
end I4SourceCurvatureDecomposition

/- Coauthored by /root/normalizer_palm_research/gaussian_reference_probe;
compiled scratch CrossLimits.lean; no scientific-review credit. -/
namespace I4SourceCurvatureDecomposition

def regularizedCurvatureCross (L r : ℝ) (i : Fin 6) : ℝ :=
  ∑' m, curvatureCoefficient L m * regularizedPinCoefficient L r i m

theorem regularizedCurvatureCross_continuous {L : ℝ} (hL : L ≠ 0) :
    Continuous (regularizedCurvatureCross L) := by
  apply continuous_pi
  intro i
  apply continuous_tsum
  · intro m
    exact continuous_const.mul (regularizedPinCoefficient_continuous hL i m)
  · exact coefficient_product_summable (curvatureCoefficient_summable hL).norm
      (confluentModeMajorant_summable hL)
  · intro m r
    rw [norm_mul]
    exact mul_le_mul_of_nonneg_left (regularizedPinCoefficient_bound hL r i m) (norm_nonneg _)

theorem regularizedCurvatureCross_zero {L : ℝ} (hL : L ≠ 0) :
    regularizedCurvatureCross L 0 = sourceContactCross L := by
  funext i
  unfold regularizedCurvatureCross
  simp_rw [regularizedPinCoefficient_zero]
  change (∑' m, sourceContactCoefficient L 6 m * sourceContactCoefficient L i.castSucc m) =
    sourceContactCovariance L i.castSucc 6
  rw [sourceContactCovariance_eq_coefficientGram hL]
  change (∑' m, _) = ∑' m, _
  exact tsum_congr (fun m => mul_comm _ _)

theorem curvatureCross_tendsto {L : ℝ} (hL : L ≠ 0) :
    Tendsto (curvatureCross L) (𝓝[>] (0 : ℝ)) (𝓝 (sourceContactCross L)) := by
  have h := (regularizedCurvatureCross_continuous hL).tendsto 0
  rw [regularizedCurvatureCross_zero hL] at h
  apply (h.mono_left nhdsWithin_le_nhds).congr'
  filter_upwards [self_mem_nhdsWithin] with r hr
  funext i
  rw [curvatureCross_coefficient hL]
  unfold regularizedCurvatureCross
  apply tsum_congr
  intro m
  rw [pinCoefficient_eq_regularized L r (ne_of_gt hr) i m]


theorem curvaturePinInverse_tendsto {L : ℝ} (hL : L ≠ 0) :
    Tendsto (fun r => (sourcePinCovarianceAt L r)⁻¹) (𝓝[>] (0 : ℝ))
      (𝓝 (sourcePinCovariance L)⁻¹) := by
  have hunit := sourcePinCovariance_isUnit hL
  have hdet0 : (sourcePinCovariance L).det ≠ 0 :=
    ((Matrix.isUnit_iff_isUnit_det _).mp hunit).ne_zero
  have hc : ContinuousAt (Ring.inverse : ℝ → ℝ) (sourcePinCovariance L).det := by
    simpa only [Ring.inverse_eq_inv'] using (continuousAt_inv₀ hdet0)
  exact (continuousAt_matrix_inv (sourcePinCovariance L) hc).tendsto.comp
    (sourcePinCovarianceAt_tendsto hL)

theorem curvatureBeta_tendsto {L : ℝ} (hL : L ≠ 0) :
    Tendsto (curvatureBeta L) (𝓝[>] (0 : ℝ))
      (𝓝 (sourceContactCross L ᵥ* (sourcePinCovariance L)⁻¹)) := by
  have hC := curvatureCross_tendsto hL
  have hG := curvaturePinInverse_tendsto hL
  apply tendsto_pi_nhds.mpr
  intro i
  change Tendsto (fun r => ∑ j, curvatureCross L r j * (sourcePinCovarianceAt L r)⁻¹ j i)
    (𝓝[>] (0 : ℝ)) (𝓝 (∑ j, sourceContactCross L j * (sourcePinCovariance L)⁻¹ j i))
  apply tendsto_finsetSum
  intro j _
  exact (((continuous_apply j).tendsto _).comp hC).mul
    (((continuous_apply i).tendsto _).comp (((continuous_apply j).tendsto _).comp hG))

theorem curvatureVariance_tendsto {L : ℝ} (hL : L ≠ 0) :
    Tendsto (curvatureVariance L) (𝓝[>] (0 : ℝ)) (𝓝 (sourceContactSchur L)) := by
  have hb := curvatureBeta_tendsto hL
  have hC := curvatureCross_tendsto hL
  have hdot : Tendsto (fun r => curvatureBeta L r ⬝ᵥ curvatureCross L r) (𝓝[>] (0 : ℝ))
      (𝓝 ((sourceContactCross L ᵥ* (sourcePinCovariance L)⁻¹) ⬝ᵥ sourceContactCross L)) := by
    apply tendsto_finsetSum
    intro i _
    exact (((continuous_apply i).tendsto _).comp hb).mul
      (((continuous_apply i).tendsto _).comp hC)
  have h : Tendsto (curvatureVariance L) (𝓝[>] (0 : ℝ))
      (𝓝 (Var[sourceContactQ L; smoothLaw 2 L] -
        (sourceContactCross L ᵥ* (sourcePinCovariance L)⁻¹) ⬝ᵥ sourceContactCross L)) :=
    tendsto_const_nhds.sub hdot
  have heq : Var[sourceContactQ L; smoothLaw 2 L] -
      (sourceContactCross L ᵥ* (sourcePinCovariance L)⁻¹) ⬝ᵥ sourceContactCross L =
      sourceContactSchur L := by
    rw [← Matrix.dotProduct_mulVec]
    unfold sourceContactSchur
    rw [sourceContactQVariance_eq_variance hL]
    rfl
  exact heq ▸ h

theorem curvatureMean_prescribed_tendsto {L : ℝ} (hL : L ≠ 0) (b : ℝ) :
    Tendsto (fun r => curvatureMean L r (sourcePrescribedPins r b)) (𝓝[>] (0 : ℝ))
      (𝓝 ((sourceContactCross L ᵥ* (sourcePinCovariance L)⁻¹) ⬝ᵥ
        ![b,0,0,0,0,2])) := by
  have hb := curvatureBeta_tendsto hL
  have hd := sourcePrescribedPins_tendsto b
  change Tendsto (fun r => ∑ i, curvatureBeta L r i * sourcePrescribedPins r b i)
    (𝓝[>] (0 : ℝ)) (𝓝 (∑ i, (sourceContactCross L ᵥ* (sourcePinCovariance L)⁻¹) i *
      (![b,0,0,0,0,2] : Fin 6 → ℝ) i))
  apply tendsto_finsetSum
  intro i _
  exact (((continuous_apply i).tendsto _).comp hb).mul
    (((continuous_apply i).tendsto _).comp hd)


theorem curvature_uniform_parameter_bounds {L : ℝ} (hL : L ≠ 0) (b : ℝ) :
    ∃ B M δ : ℝ, 0 ≤ B ∧ 0 ≤ M ∧ 0 < δ ∧ δ ≤ 1 ∧
      ∀ r : ℝ, 0 < r → r < δ →
        IsUnit (sourcePinCovarianceAt L r) ∧
        sourceContactSchur L / 2 ≤ curvatureVariance L r ∧
        (∀ i, |curvatureBeta L r i| ≤ B) ∧
        |curvatureMean L r (sourcePrescribedPins r b)| ≤ M := by
  let β0 := sourceContactCross L ᵥ* (sourcePinCovariance L)⁻¹
  let m0 := β0 ⬝ᵥ (![b,0,0,0,0,2] : Fin 6 → ℝ)
  let B := ‖β0‖ + 1
  let M := |m0| + 1
  have hτ : ∀ᶠ r in 𝓝[>] (0 : ℝ), sourceContactSchur L/2 < curvatureVariance L r := by
    apply (curvatureVariance_tendsto hL).eventually
    exact lt_mem_nhds (by linarith [sourceContactSchur_pos hL])
  have hβ : ∀ᶠ r in 𝓝[>] (0 : ℝ), ‖curvatureBeta L r‖ < B :=
    (curvatureBeta_tendsto hL).norm.eventually (gt_mem_nhds (by dsimp [B]; linarith))
  have hm : ∀ᶠ r in 𝓝[>] (0 : ℝ), |curvatureMean L r (sourcePrescribedPins r b)| < M := by
    simpa only [Real.norm_eq_abs] using (curvatureMean_prescribed_tendsto hL b).norm.eventually
      (gt_mem_nhds (by dsimp [M]; linarith))
  have hu := (sourceEndpoint_parameter_limits hL b).1
  have hall : ∀ᶠ r in 𝓝[>] (0 : ℝ),
      IsUnit (sourcePinCovarianceAt L r) ∧
      sourceContactSchur L/2 < curvatureVariance L r ∧
      ‖curvatureBeta L r‖ < B ∧ |curvatureMean L r (sourcePrescribedPins r b)| < M := by
    filter_upwards [hu,hτ,hβ,hm] with r hr ht hb hm
    exact ⟨hr,ht,hb,hm⟩
  obtain ⟨δ,hδ,hbound⟩ := mem_nhdsGT_iff_exists_Ioo_subset.mp hall
  refine ⟨B,M,min δ 1,by dsimp [B]; positivity,by dsimp [M]; positivity,
    lt_min hδ (by norm_num),min_le_right _ _,?_⟩
  intro r hr hrδ
  obtain ⟨hunit,ht,hbeta,hmean⟩ := hbound ⟨hr,lt_of_lt_of_le hrδ (min_le_left _ _)⟩
  refine ⟨hunit,ht.le,?_,hmean.le⟩
  intro i
  exact (show |curvatureBeta L r i| ≤ ‖curvatureBeta L r‖ by
    simpa only [Real.norm_eq_abs] using norm_le_pi_norm (curvatureBeta L r) i).trans hbeta.le

end I4SourceCurvatureDecomposition

namespace I4SourceCurvatureDecomposition

theorem curvatureZ_measurable (L r : ℝ) : Measurable (curvatureZ L r) :=
  (scalarSeries_measurable _).comp measurable_subtype_coe

theorem sourceContactQ_measurable {L : ℝ} (hL : L ≠ 0) : Measurable (sourceContactQ L) := by
  have h : sourceContactQ L = fun ω => scalarSeries (curvatureCoefficient L) ω.val :=
    funext (sourceContactQ_series hL)
  rw [h]
  exact (scalarSeries_measurable _).comp measurable_subtype_coe

theorem curvatureZ_hasLaw {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (hG : IsUnit (sourcePinCovarianceAt L r)) (hτ : 0 < curvatureVariance L r) :
    HasLaw (curvatureZ L r) (gaussianReal 0 1) (smoothLaw 2 L) :=
  unitDirection_hasLaw hL _ (curvatureDirection_summable hL r)
    (curvatureDirection_normSquared hL r hG hτ)

theorem curvatureDirection_goodSample {L : ℝ} (hL : L ≠ 0) (r : ℝ) :
    goodSample 2 L (curvatureDirection L r) := by
  intro n
  exact coefficient_product_summable (orderModeBound_summable n 2 hL)
    (curvatureDirection_summable hL r).abs

def curvatureShift {L : ℝ} (hL : L ≠ 0) (r t : ℝ) (ω : SmoothSample 2 L) : SmoothSample 2 L :=
  ⟨fun m => ω.val m + curvatureDirection L r m * t, by
    apply goodSample_add _ _ ω.property
    intro n
    simpa only [abs_mul, mul_assoc] using ((curvatureDirection_goodSample hL r) n).mul_right |t|⟩

@[simp] theorem curvatureShift_val {L : ℝ} (hL : L ≠ 0) (r t : ℝ)
    (ω : SmoothSample 2 L) (m : SourceMode 2) :
    (curvatureShift hL r t ω).val m = ω.val m + curvatureDirection L r m * t := rfl

theorem curvatureShift_measurable {L : ℝ} (hL : L ≠ 0) (r : ℝ) :
    Measurable (fun p : ℝ × SmoothSample 2 L => curvatureShift hL r p.1 p.2) := by
  apply Measurable.subtype_mk
  apply Measurable.of_eval
  intro m
  exact ((measurable_pi_apply m).comp (measurable_subtype_coe.comp measurable_snd)).add
    (measurable_const.mul measurable_fst)

def curvatureResidualSample {L : ℝ} (hL : L ≠ 0) (r : ℝ) (ω : SmoothSample 2 L) : SmoothSample 2 L :=
  curvatureShift hL r (-curvatureZ L r ω) ω

def curvatureResidualLaw {L : ℝ} (hL : L ≠ 0) (r : ℝ) : Measure (SmoothSample 2 L) :=
  (smoothLaw 2 L).map (curvatureResidualSample hL r)

theorem curvatureResidualSample_measurable {L : ℝ} (hL : L ≠ 0) (r : ℝ) :
    Measurable (curvatureResidualSample hL r) :=
  (curvatureShift_measurable hL r).comp ((curvatureZ_measurable L r).neg.prodMk measurable_id)

instance curvatureResidualLaw_isProbabilityMeasure {L : ℝ} (hL : L ≠ 0) (r : ℝ) :
    IsProbabilityMeasure (curvatureResidualLaw hL r) := by
  have : IsProbabilityMeasure (smoothLaw 2 L) := smoothLaw_isProbabilityMeasure 2 hL
  unfold curvatureResidualLaw
  infer_instance

private theorem scalarSeries_curvatureShift {L : ℝ} (hL : L ≠ 0) (r t : ℝ)
    (ω : SmoothSample 2 L) (a : SourceMode 2 → ℝ) (ha : Summable a)
    (hω : Summable (fun m => a m * ω.val m)) :
    scalarSeries a (curvatureShift hL r t ω).val =
      scalarSeries a ω.val + (∑' m, a m * curvatureDirection L r m) * t := by
  have hs := ((coefficient_product_summable ha (curvatureDirection_summable hL r)).hasSum).mul_right t
  have ht := hω.hasSum.add hs
  change (∑' m, a m * (ω.val m + curvatureDirection L r m * t)) = _
  convert ht.tsum_eq using 1
  · apply tsum_congr
    intro m
    ring
  · rfl

theorem sourceConfluentPinsAt_curvatureShift {L : ℝ} (hL : L ≠ 0) (r t : ℝ)
    (hG : IsUnit (sourcePinCovarianceAt L r)) (ω : SmoothSample 2 L) :
    sourceConfluentPinsAt L r (curvatureShift hL r t ω) = sourceConfluentPinsAt L r ω := by
  rw [sourceConfluentPinsAt_series hL r (curvatureShift hL r t ω), sourceConfluentPinsAt_series hL r ω]
  funext i
  change scalarSeries (pinCoefficient L r i) (curvatureShift hL r t ω).val =
    scalarSeries (pinCoefficient L r i) ω.val
  rw [scalarSeries_curvatureShift hL r t ω _ (pinCoefficient_summable hL r i)
    (pinCoefficient_weighted_summable hL r ω i), curvatureDirection_pin_orthogonal hL r hG i]
  simp

theorem sourceContactQ_curvatureShift {L : ℝ} (hL : L ≠ 0) (r t : ℝ)
    (hτ : 0 < curvatureVariance L r) (ω : SmoothSample 2 L) :
    sourceContactQ L (curvatureShift hL r t ω) = sourceContactQ L ω + curvatureSigma L r * t := by
  rw [sourceContactQ_series hL (curvatureShift hL r t ω), sourceContactQ_series hL ω,
    scalarSeries_curvatureShift hL r t ω _ (curvatureCoefficient_summable hL)
      (curvatureCoefficient_weighted_summable hL ω), curvatureDirection_q_pairing hL r hτ]

theorem curvatureZ_curvatureShift {L : ℝ} (hL : L ≠ 0) (r t : ℝ)
    (hG : IsUnit (sourcePinCovarianceAt L r)) (hτ : 0 < curvatureVariance L r)
    (ω : SmoothSample 2 L) :
    curvatureZ L r (curvatureShift hL r t ω) = curvatureZ L r ω + t := by
  unfold curvatureZ
  rw [scalarSeries_curvatureShift hL r t ω _ (curvatureDirection_summable hL r)
    (curvatureDirection_weighted_summable hL r ω)]
  have h : (∑' m, curvatureDirection L r m * curvatureDirection L r m) = 1 := by
    simpa only [pow_two] using curvatureDirection_normSquared hL r hG hτ
  rw [h, one_mul]

theorem curvatureResidualSample_pins {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (hG : IsUnit (sourcePinCovarianceAt L r)) (ω : SmoothSample 2 L) :
    sourceConfluentPinsAt L r (curvatureResidualSample hL r ω) = sourceConfluentPinsAt L r ω :=
  sourceConfluentPinsAt_curvatureShift hL r _ hG ω

theorem curvatureResidualSample_Z {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (hG : IsUnit (sourcePinCovarianceAt L r)) (hτ : 0 < curvatureVariance L r)
    (ω : SmoothSample 2 L) : curvatureZ L r (curvatureResidualSample hL r ω) = 0 := by
  rw [curvatureResidualSample, curvatureZ_curvatureShift hL r _ hG hτ]
  exact add_neg_cancel _

theorem curvatureResidualSample_inclusion {L : ℝ} (hL : L ≠ 0) (r : ℝ) (ω : SmoothSample 2 L) :
    (curvatureResidualSample hL r ω).val = unitDirectionCoefficientResidual (curvatureDirection L r) ω := by
  funext m
  change ω.val m + curvatureDirection L r m * (-curvatureZ L r ω) = _
  unfold unitDirectionCoefficientResidual unitDirection curvatureZ
  ring

theorem curvatureResidualSample_indepFun {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (hG : IsUnit (sourcePinCovarianceAt L r)) (hτ : 0 < curvatureVariance L r) :
    IndepFun (curvatureZ L r) (curvatureResidualSample hL r) (smoothLaw 2 L) := by
  obtain ⟨q,hq,hret⟩ := exists_measurable_sampleProjection 2 L
  have hi := (unitDirectionCoefficientResidual_indepFun hL (curvatureDirection L r)
    (curvatureDirection_summable hL r) (curvatureDirection_normSquared hL r hG hτ)).comp measurable_id hq
  have heq : q ∘ (fun ω => unitDirectionCoefficientResidual (curvatureDirection L r) ω) =
      curvatureResidualSample hL r := by
    funext ω
    rw [Function.comp_apply, ← curvatureResidualSample_inclusion hL r ω]
    exact hret _
  change IndepFun (unitDirection (curvatureDirection L r)) (curvatureResidualSample hL r) (smoothLaw 2 L)
  simpa only [Function.id_comp, heq] using hi

theorem curvatureResidualSample_joint_map {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (hG : IsUnit (sourcePinCovarianceAt L r)) (hτ : 0 < curvatureVariance L r) :
    (smoothLaw 2 L).map (fun ω => (curvatureResidualSample hL r ω, curvatureZ L r ω)) =
      (curvatureResidualLaw hL r).prod (gaussianReal 0 1) := by
  have : IsProbabilityMeasure (smoothLaw 2 L) := smoothLaw_isProbabilityMeasure 2 hL
  rw [(curvatureResidualSample_indepFun hL r hG hτ).symm.map_prod_eq_prod_map_map
    (curvatureResidualSample_measurable hL r).aemeasurable (curvatureZ_measurable L r).aemeasurable,
    (curvatureZ_hasLaw hL r hG hτ).map_eq]
  rfl

theorem sourceContactQ_posteriorSample {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (x : Fin 6 → ℝ) (ω : SmoothSample 2 L) :
    sourceContactQ L (posteriorSample hL r x ω) = sourceContactQ L ω +
      curvatureMean L r (x - sourceConfluentPinsAt L r ω) := by
  rw [sourceContactQ_series hL (posteriorSample hL r x ω), sourceContactQ_series hL ω]
  change scalarSeries (curvatureCoefficient L)
    (fun m => ω.val m + ∑ i, pinCoefficient L r i m *
      (((sourcePinCovarianceAt L r)⁻¹ *ᵥ (x - sourceConfluentPinsAt L r ω)) i)) = _
  rw [scalarSeries_add_finiteShift _ _ _ _ (curvatureCoefficient_summable hL)
    (pinCoefficient_summable hL r) (curvatureCoefficient_weighted_summable hL ω)]
  simp_rw [← curvatureCross_coefficient hL r]
  change _ + curvatureCross L r ⬝ᵥ (sourcePinCovarianceAt L r)⁻¹ *ᵥ _ = _
  rw [Matrix.dotProduct_mulVec]
  rfl

theorem sourceContactQ_posteriorSample_Z {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (hτ : 0 < curvatureVariance L r) (x : Fin 6 → ℝ) (ω : SmoothSample 2 L) :
    sourceContactQ L (posteriorSample hL r x ω) = curvatureMean L r x +
      curvatureSigma L r * curvatureZ L r ω := by
  have hz := (div_eq_iff (curvatureSigma_pos hτ).ne').mp (curvatureZ_eq hL r ω).symm
  rw [sourceContactQ_posteriorSample hL r x ω]
  simp only [curvatureMean, dotProduct_sub] at *
  nlinarith only [hz]

theorem sourceContactQ_posteriorResidual {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (hG : IsUnit (sourcePinCovarianceAt L r)) (hτ : 0 < curvatureVariance L r)
    (x : Fin 6 → ℝ) (ω : SmoothSample 2 L) :
    sourceContactQ L (posteriorSample hL r x (curvatureResidualSample hL r ω)) = curvatureMean L r x := by
  rw [sourceContactQ_posteriorSample_Z hL r hτ x, curvatureResidualSample_Z hL r hG hτ, mul_zero, add_zero]

theorem curvaturePosterior_reconstruction {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (hG : IsUnit (sourcePinCovarianceAt L r)) (x : Fin 6 → ℝ) (ω : SmoothSample 2 L) :
    curvatureShift hL r (curvatureZ L r ω)
      (posteriorSample hL r x (curvatureResidualSample hL r ω)) = posteriorSample hL r x ω := by
  apply Subtype.ext
  funext m
  simp only [curvatureShift_val, posteriorSample_val]
  rw [curvatureResidualSample_pins hL r hG]
  simp only [curvatureResidualSample, curvatureShift_val]
  ring

def curvatureReconstruct {L : ℝ} (hL : L ≠ 0) (r : ℝ) (x : Fin 6 → ℝ)
    (ρ : SmoothSample 2 L) (q : ℝ) : SmoothSample 2 L :=
  curvatureShift hL r ((q - sourceContactQ L (posteriorSample hL r x ρ)) / curvatureSigma L r)
    (posteriorSample hL r x ρ)

theorem curvatureReconstruct_measurable {L : ℝ} (hL : L ≠ 0) (r : ℝ) (x : Fin 6 → ℝ) :
    Measurable (fun p : SmoothSample 2 L × ℝ => curvatureReconstruct hL r x p.1 p.2) := by
  have hp : Measurable (fun p : SmoothSample 2 L × ℝ => posteriorSample hL r x p.1) :=
    (posteriorSample_measurable hL r).comp (measurable_const.prodMk measurable_fst)
  exact (curvatureShift_measurable hL r).comp
    (((measurable_snd.sub ((sourceContactQ_measurable hL).comp hp)).div_const _).prodMk hp)

theorem curvatureReconstruct_pins {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (hG : IsUnit (sourcePinCovarianceAt L r)) (x : Fin 6 → ℝ) (ρ : SmoothSample 2 L) (q : ℝ) :
    sourceConfluentPinsAt L r (curvatureReconstruct hL r x ρ q) = x := by
  rw [curvatureReconstruct, sourceConfluentPinsAt_curvatureShift hL r _ hG,
    sourceConfluentPinsAt_posteriorSample hL r hG]

theorem curvatureReconstruct_Q {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (hτ : 0 < curvatureVariance L r) (x : Fin 6 → ℝ) (ρ : SmoothSample 2 L) (q : ℝ) :
    sourceContactQ L (curvatureReconstruct hL r x ρ q) = q := by
  rw [curvatureReconstruct, sourceContactQ_curvatureShift hL r _ hτ]
  have hs := (curvatureSigma_pos hτ).ne'
  field_simp [hs]; ring

theorem curvatureReconstruct_residual_image {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (hG : IsUnit (sourcePinCovarianceAt L r)) (hτ : 0 < curvatureVariance L r)
    (x : Fin 6 → ℝ) (ω : SmoothSample 2 L) :
    curvatureReconstruct hL r x (curvatureResidualSample hL r ω)
      (curvatureMean L r x + curvatureSigma L r * curvatureZ L r ω) = posteriorSample hL r x ω := by
  unfold curvatureReconstruct
  rw [sourceContactQ_posteriorResidual hL r hG hτ x ω]
  have hs : (curvatureMean L r x + curvatureSigma L r * curvatureZ L r ω - curvatureMean L r x) /
      curvatureSigma L r = curvatureZ L r ω := by
    field_simp [(curvatureSigma_pos hτ).ne']; ring
  rw [hs]
  exact curvaturePosterior_reconstruction hL r hG x ω

end I4SourceCurvatureDecomposition

/- Uniform direction envelope coauthored by /root/normalizer_palm_research/gaussian_reference_probe. -/
namespace I4SourceCurvatureDecomposition

def curvatureDirectionEnvelope (L B : ℝ) (m : SourceMode 2) : ℝ :=
  (|curvatureCoefficient L m| + 6*B*confluentModeMajorant L m) *
    ((Real.sqrt (sourceContactSchur L/2))⁻¹ + (Real.sqrt (sourceContactSchur L/2))⁻¹^2)

theorem curvatureDirectionEnvelope_nonneg {L : ℝ} (B : ℝ) (hB : 0 ≤ B)
    (m : SourceMode 2) : 0 ≤ curvatureDirectionEnvelope L B m := by
  unfold curvatureDirectionEnvelope
  have hA := confluentModeMajorant_nonneg L m
  positivity

theorem curvatureDirectionEnvelope_summable {L : ℝ} (hL : L ≠ 0) (B : ℝ) :
    Summable (curvatureDirectionEnvelope L B) := by
  exact ((curvatureCoefficient_summable hL).abs.add
    ((confluentModeMajorant_summable hL).mul_left (6*B))).mul_right _

theorem curvatureDirectionEnvelope_weighted_summable {L : ℝ} (hL : L ≠ 0) (B : ℝ) (n : ℕ) :
    Summable (fun m => orderModeBound n 2 L m * curvatureDirectionEnvelope L B m) :=
  coefficient_product_summable (orderModeBound_summable n 2 hL)
    (curvatureDirectionEnvelope_summable hL B)

theorem curvatureDirection_envelope_at {L : ℝ} (hL : L ≠ 0) (r B : ℝ)
    (hr : r ≠ 0) (hB : 0 ≤ B) (hβ : ∀ i, |curvatureBeta L r i| ≤ B)
    (hτ : sourceContactSchur L/2 ≤ curvatureVariance L r) (m : SourceMode 2) :
    |curvatureDirection L r m| ≤ curvatureDirectionEnvelope L B m ∧
      |curvatureDirection L r m| / curvatureSigma L r ≤ curvatureDirectionEnvelope L B m := by
  let s := Real.sqrt (sourceContactSchur L/2)
  let D := |curvatureCoefficient L m| + 6*B*confluentModeMajorant L m
  have hs : 0 < s := Real.sqrt_pos.mpr (by linarith [sourceContactSchur_pos hL])
  have hσ : s ≤ curvatureSigma L r := Real.sqrt_le_sqrt hτ
  have hσpos : 0 < curvatureSigma L r := hs.trans_le hσ
  have hD : 0 ≤ D := by
    dsimp [D]
    have hA := confluentModeMajorant_nonneg L m
    positivity
  have hres : |curvatureResidualCoefficient L r m| ≤ D := by
    unfold curvatureResidualCoefficient
    calc
      _ ≤ |curvatureCoefficient L m| + |∑ i, curvatureBeta L r i * pinCoefficient L r i m| :=
        abs_sub _ _
      _ ≤ |curvatureCoefficient L m| + ∑ i, |curvatureBeta L r i * pinCoefficient L r i m| :=
        add_le_add le_rfl (Finset.abs_sum_le_sum_abs _ _)
      _ ≤ |curvatureCoefficient L m| + ∑ _i : Fin 6, B*confluentModeMajorant L m := by
        apply add_le_add le_rfl
        apply Finset.sum_le_sum
        intro i _
        rw [abs_mul]
        exact mul_le_mul (hβ i) (pinCoefficient_abs_le hL r hr i m) (abs_nonneg _) hB
      _ = D := by dsimp [D]; simp; ring
  have hdir : |curvatureDirection L r m| ≤ D/s := by
    rw [curvatureDirection, abs_div, abs_of_pos hσpos]
    exact (div_le_div_of_nonneg_right hres hσpos.le).trans
      (div_le_div_of_nonneg_left hD hs hσ)
  have hfirst : D/s ≤ curvatureDirectionEnvelope L B m := by
    change D/s ≤ D*(s⁻¹+s⁻¹^2)
    rw [div_eq_mul_inv, mul_add]
    exact le_add_of_nonneg_right (mul_nonneg hD (sq_nonneg _))
  have hsecond : (D/s)/s ≤ curvatureDirectionEnvelope L B m := by
    change (D/s)/s ≤ D*(s⁻¹+s⁻¹^2)
    have heq : (D/s)/s = D*s⁻¹^2 := by ring
    rw [heq, mul_add]
    exact le_add_of_nonneg_left (mul_nonneg hD (inv_nonneg.mpr hs.le))
  refine ⟨hdir.trans hfirst, ?_⟩
  calc
    _ ≤ (D/s)/curvatureSigma L r := div_le_div_of_nonneg_right hdir hσpos.le
    _ ≤ (D/s)/s := div_le_div_of_nonneg_left (div_nonneg hD hs.le) hs hσ
    _ ≤ _ := hsecond

theorem curvatureDirection_uniform_envelope {L : ℝ} (hL : L ≠ 0) (b : ℝ) :
    ∃ δ : ℝ, 0 < δ ∧ δ ≤ 1 ∧ ∃ U : SourceMode 2 → ℝ,
      (∀ m, 0 ≤ U m) ∧ Summable U ∧
      (∀ n : ℕ, Summable (fun m => orderModeBound n 2 L m * U m)) ∧
      ∀ r : ℝ, 0 < r → r < δ → ∀ m,
        |curvatureDirection L r m| ≤ U m ∧
          |curvatureDirection L r m| / curvatureSigma L r ≤ U m := by
  obtain ⟨B,M,δ,hB,_hM,hδ,hδ1,hbound⟩ := curvature_uniform_parameter_bounds hL b
  refine ⟨δ,hδ,hδ1,curvatureDirectionEnvelope L B,
    curvatureDirectionEnvelope_nonneg B hB,curvatureDirectionEnvelope_summable hL B,
    curvatureDirectionEnvelope_weighted_summable hL B,?_⟩
  intro r hr hrδ m
  obtain ⟨_hG,hτ,hβ,_hm⟩ := hbound r hr hrδ
  exact curvatureDirection_envelope_at hL r B (ne_of_gt hr) hB hβ hτ m
end I4SourceCurvatureDecomposition

namespace I4SourceCurvatureDecomposition

theorem curvatureAffine_gaussian {L r : ℝ} (hτ : 0 < curvatureVariance L r) (m : ℝ) :
    (gaussianReal 0 1).map (fun z => m + curvatureSigma L r * z) =
      gaussianReal m (curvatureVariance L r).toNNReal := by
  calc
    _ = ((gaussianReal 0 1).map (curvatureSigma L r * ·)).map (m + ·) := by
      rw [Measure.map_map (by fun_prop) (by fun_prop)]
      rfl
    _ = gaussianReal m (⟨curvatureSigma L r ^ 2, sq_nonneg _⟩ * 1) := by
      rw [gaussianReal_map_const_mul, gaussianReal_map_const_add]
      simp
    _ = _ := by
      congr 1
      apply NNReal.coe_injective
      simp only [NNReal.coe_mul, NNReal.coe_mk, NNReal.coe_one, mul_one,
        Real.coe_toNNReal _ hτ.le]
      exact curvatureSigma_sq hτ

/-- Exact independent residual/curvature law at every pin, including null pins. -/
theorem curvatureResidual_curvature_joint_map {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (hG : IsUnit (sourcePinCovarianceAt L r)) (hτ : 0 < curvatureVariance L r) (x : Fin 6 → ℝ) :
    (smoothLaw 2 L).map (fun ω => (curvatureResidualSample hL r ω,
      curvatureMean L r x + curvatureSigma L r * curvatureZ L r ω)) =
      (curvatureResidualLaw hL r).prod
        (gaussianReal (curvatureMean L r x) (curvatureVariance L r).toNNReal) := by
  have : IsProbabilityMeasure (smoothLaw 2 L) := smoothLaw_isProbabilityMeasure 2 hL
  let f : ℝ → ℝ := fun z => curvatureMean L r x + curvatureSigma L r * z
  have hf : Measurable f := by fun_prop
  calc
    _ = ((smoothLaw 2 L).map (fun ω => (curvatureResidualSample hL r ω, curvatureZ L r ω))).map
        (Prod.map id f) := by
      rw [Measure.map_map (measurable_id.prodMap hf)
        ((curvatureResidualSample_measurable hL r).prodMk (curvatureZ_measurable L r))]
      rfl
    _ = ((curvatureResidualLaw hL r).prod (gaussianReal 0 1)).map (Prod.map id f) := by
      rw [curvatureResidualSample_joint_map hL r hG hτ]
    _ = (curvatureResidualLaw hL r).prod ((gaussianReal 0 1).map f) := by
      simpa only [Measure.map_id] using
        (Measure.map_prod_map (curvatureResidualLaw hL r) (gaussianReal 0 1) measurable_id hf).symm
    _ = _ := by rw [curvatureAffine_gaussian hτ]

/-- This literal measure identity reconstructs the full conditioned smooth sample,
not merely a finite-dimensional conditional-law version. -/
theorem sourceSmoothKernel_eq_curvatureProduct {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (hG : IsUnit (sourcePinCovarianceAt L r)) (hτ : 0 < curvatureVariance L r) (x : Fin 6 → ℝ) :
    sourceSmoothKernel hL r x =
      ((curvatureResidualLaw hL r).prod
        (gaussianReal (curvatureMean L r x) (curvatureVariance L r).toNNReal)).map
          (fun p => curvatureReconstruct hL r x p.1 p.2) := by
  rw [← curvatureResidual_curvature_joint_map hL r hG hτ x,
    Measure.map_map (curvatureReconstruct_measurable hL r x)
      ((curvatureResidualSample_measurable hL r).prodMk
        (measurable_const.add (measurable_const.mul (curvatureZ_measurable L r)))),
    sourceSmoothKernel_apply hL r x]
  congr 1
  funext ω
  exact (curvatureReconstruct_residual_image hL r hG hτ x ω).symm

/-- Scalar-first product order for one-dimensional density integration. -/
theorem sourceSmoothKernel_eq_curvatureProduct_swap {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (hG : IsUnit (sourcePinCovarianceAt L r)) (hτ : 0 < curvatureVariance L r) (x : Fin 6 → ℝ) :
    sourceSmoothKernel hL r x =
      ((gaussianReal (curvatureMean L r x) (curvatureVariance L r).toNNReal).prod
        (curvatureResidualLaw hL r)).map (fun p => curvatureReconstruct hL r x p.2 p.1) := by
  have hs : Measurable (fun p : ℝ × SmoothSample 2 L => curvatureReconstruct hL r x p.2 p.1) :=
    (curvatureReconstruct_measurable hL r x).comp measurable_swap
  rw [sourceSmoothKernel_eq_curvatureProduct hL r hG hτ x,
    ← Measure.prod_swap (μ := curvatureResidualLaw hL r),
    Measure.map_map hs measurable_swap]
  rfl

end I4SourceCurvatureDecomposition
