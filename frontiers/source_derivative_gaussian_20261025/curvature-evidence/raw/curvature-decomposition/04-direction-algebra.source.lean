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
open I4GaussianRegressionLimits MeasureTheory ProbabilityTheory Matrix Filter
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
    apply Finset.sum_congr rfl
    intro i _
    rw [congrFun (sourceConfluentPinsAt_series hL r ω) i]
  simpa only [scalarSeries, div_mul_eq_mul_div, tsum_div_const] using congrArg
    (fun t : ℝ => t / curvatureSigma L r) hd

end I4SourceCurvatureDecomposition
